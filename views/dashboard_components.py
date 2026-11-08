import customtkinter as ctk
from tkinter import messagebox


# PENGATURAN TAMPILAN
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")


# WARNA
WARNA_BG = "#F2F5F8"
WARNA_PUTIH = "#FFFFFF"
WARNA_BIRU = "#367FB5"
WARNA_BIRU_TUA = "#24527A"
WARNA_TEKS = "#333333"
WARNA_ABU = "#777777"
WARNA_GARIS = "#DCE3E9"
WARNA_HIJAU = "#39865B"
WARNA_MERAH = "#C94C4C"


# KOMPONEN TOMBOL
def buat_tombol(parent, teks, command, warna=WARNA_BIRU,
                hover="#286A9D", lebar=150):
    return ctk.CTkButton(
        parent,
        text=teks,
        command=command,
        width=lebar,
        height=38,
        corner_radius=7,
        fg_color=warna,
        hover_color=hover,
        font=("Arial", 12)
    )


# KOMPONEN JUDUL
def buat_judul(parent, teks, ukuran=20):
    return ctk.CTkLabel(
        parent,
        text=teks,
        font=("Arial", ukuran, "bold"),
        text_color=WARNA_TEKS
    )


# KOMPONEN KARTU
def buat_kartu(parent, judul):
    frame = ctk.CTkFrame(
        parent,
        fg_color=WARNA_PUTIH,
        corner_radius=8,
        border_width=1,
        border_color=WARNA_GARIS
    )

    ctk.CTkLabel(
        frame,
        text=judul,
        font=("Arial", 14, "bold"),
        text_color=WARNA_BIRU_TUA
    ).pack(anchor="w", padx=18, pady=(16, 10))

    return frame


# INFORMASI MODUL
def tampilkan_modul_belum_terhubung(nama_modul):
    messagebox.showinfo(
        "Informasi Modul",
        f"Menu {nama_modul} belum dihubungkan dengan controller."
    )