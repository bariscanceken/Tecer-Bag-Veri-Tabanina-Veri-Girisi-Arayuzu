import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from mustisp import *

uygulama = QApplication(sys.argv)
pencere = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(pencere)
pencere.show()

import sqlite3
baglanti = sqlite3.connect("tecermaliveri.db")
islem = baglanti.cursor()
baglanti.commit()

table = islem.execute("create table if not exists tecermalitablo (kayitNo int, tarih int, ekleyen text, gelen int, giden int, sirket text , aciklama text) ")
baglanti.commit()

def kayit_ekle():
    Ekleyen = ui.cmbEkleyen.currentText()
    Kayitno = int(ui.lineKayitNo.text())
    Tarih = ui.lineTarih.text()
    Gelen = int(ui.lineGelen.text())
    Giden = int(ui.lineGiden.text())
    Sirket = ui.lineSirket.text()
    Aciklama = ui.lineAciklama.text()


    try:
        ekle = "insert into tecermalitablo (KayitNo , Tarih , Ekleyen , Gelen , Giden , Sirket , Aciklama) values (?,?,?,?,?,?,?)"
        islem.execute(ekle,(Kayitno,Tarih,Ekleyen,Gelen,Giden,Sirket,Aciklama))
        baglanti.commit()
        ui.statusbar.showMessage("Kayıt Eklendi! ", 2000)
    except Exception as error:
        ui.statusbar.showMessage("Kayıt Eklenemedi :(! "+str(error))


def kayit_listele():
    ui.tblTabloListele.clear()
    ui.tblTabloListele.setHorizontalHeaderLabels(("Kayıt No", "Tarih", "Ekleyen", "Gelen Miktar", "Giden Miktar", "Şirket Adı", "Açıklama"))
    ui.tblTabloListele.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    
    sorgu = "select * from tecermalitablo"
    islem.execute(sorgu)

    for indexSatir , kayitNumarasi in enumerate(islem):
        for indexSutun, kayitSutun in enumerate(kayitNumarasi):
            ui.tblTabloListele.setItem(indexSatir,indexSutun,QTableWidgetItem(str(kayitSutun)))

kayit_listele()

def gore_listele():
    listelenecek_katagori = ui.cmbListele.currentText()
    
    if listelenecek_katagori == "Tüm Kategoriler":
        sorgu = "SELECT * FROM tecermalitablo"

    else:
        sorgu = f"SELECT kayitNo , {listelenecek_katagori} FROM tecermalitablo"

    try:
        islem.execute(sorgu)
        ui.tblTabloListele.clear()
        
        columns = [desc[0] for desc in islem.description]
        ui.tblTabloListele.setColumnCount(len(columns))
        ui.tblTabloListele.setHorizontalHeaderLabels(columns)
        
        for indexSatir, kayitnumarasi in enumerate(islem.fetchall()):
            ui.tblTabloListele.insertRow(indexSatir)
            for indexsutun, kayitsutun in enumerate(kayitnumarasi):
                ui.tblTabloListele.setItem(indexSatir, indexsutun, QTableWidgetItem(str(kayitsutun)))
    except Exception as error:
        ui.statusbar.showMessage(f"Veri getirilemedi! :(! {error}", 2000)


def kayit_sil ():
    silmesaj = QMessageBox.question(pencere,"Silme Onayı","Silmek İstediğinizden Emin Misiniz?",QMessageBox.Yes|QMessageBox.No)
    if silmesaj == QMessageBox.Yes:
        secilen_kayit = ui.tblTabloListele.selectedItems()
        silinecek_kayit = secilen_kayit[0].text()

        sorgu = "delete from tecermalitablo where kayitNo = ?"
        try:
            islem.execute(sorgu,(silinecek_kayit,))
            baglanti.commit()
            ui.statusbar.showMessage("Kayıt Sİlindi")
            kayit_listele()
        except Exception as error:
            ui.statusbar.showMessage("Kayıt Silinirken Hata Çıktı === "+str(error))
    else :
        ui.statusbar.showMessage("Silmekten Vazgeçildi")
        

def kayitguncelle():
    guncelleme_mesaj = QMessageBox.question(pencere, "Güncelleme Onayı", "Kaydı Güncellemek İstediğinize Emin Misiniz?", QMessageBox.Yes | QMessageBox.No)
    if guncelleme_mesaj == QMessageBox.Yes:
        try:
            kayitNo = ui.lineKayitNo.text()
            tarih = ui.lineTarih.text()
            ekleyen = ui.cmbEkleyen.currentText()
            gelen = ui.lineGelen.text()
            giden = ui.lineGiden.text()
            sirket = ui.lineSirket.text()
            aciklama = ui.lineAciklama.text()

            updates = []
            values = []

            if tarih:
                updates.append("Tarih = ?")
                values.append(tarih)
            if ekleyen:
                updates.append("Ekleyen = ?")
                values.append(ekleyen)
            if gelen:
                updates.append("Gelen = ?")
                values.append(gelen)
            if giden:
                updates.append("Giden = ?")
                values.append(giden)
            if sirket:
                updates.append("Sirket = ?")
                values.append(sirket)
            if aciklama:
                updates.append("Aciklama = ?")
                values.append(aciklama)

            if not updates:
                ui.statusbar.showMessage("Güncellenmesi gereken bir bilgi girilmedi!")
                return

            set_clause = ", ".join(updates)
            sorgu = f"UPDATE tecermalitablo SET {set_clause} WHERE KayitNo = ?"
            values.append(kayitNo)

            islem.execute(sorgu, tuple(values))
            baglanti.commit()
            ui.statusbar.showMessage("Kayıt Güncellendi!")
            kayit_listele()
        except Exception as error:
            ui.statusbar.showMessage(f"Kayıt Güncellenirken Hata Çıktı! {error}", 2000)
    else:
        ui.statusbar.showMessage("Güncellemeden Vazgeçildi")





#butonlar
ui.btnEkle.clicked.connect(kayit_ekle)
ui.btnListele.clicked.connect(kayit_listele)
ui.btnGoreListele.clicked.connect(gore_listele)
ui.btnSil.clicked.connect(kayit_sil)
ui.btnDuzenle.clicked.connect(kayitguncelle)


sys.exit(uygulama.exec_())
