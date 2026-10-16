import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font as tkfont


#Warna tema
TEAL = "#008080"
BUTTER = "#FFEDA8"
GELAP = "#005F5F"
FONT = "Poppins"


#n didefinisikan sebagai pilihan bunga
FREKUENSI = {"Tahunan (1x)": 1, "Triwulanan (4x)": 4, "Bulanan (12x)": 12}


def hitung_fv(pv, r, n, t):
    #Rumus interest compounding: FV = PV x (1 + r/n) ^ (n x t)
    return pv * (1 + r / n) ** (n * t)


def rupiah(angka):
    #1234567.8 -> Rp 1.234.567,80
    teks = f"{angka:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return "Rp " + teks


def hitung():
    try:
        pv = float(entry_pv.get().replace(",", "."))
        bunga = float(entry_bunga.get().replace(",", "."))
        t = float(entry_waktu.get().replace(",", "."))
    except ValueError:
        messagebox.showerror("Oops", "Semua kolom harus diisi dengan angka yang valid.")
        return


    if pv < 0 or t < 0:
        messagebox.showerror("Oops", "Uang awal dan jangka waktu tidak boleh negatif.")
        return


    n = FREKUENSI.get(combo.get())
    if n is None:
        messagebox.showerror("Oops", "Pilih frekuensi bunga dulu ya.")
        return


    try:
        r = bunga / 100  #5% jadi 0,05
        fv = hitung_fv(pv, r, n, t)
    except OverflowError:
        messagebox.showerror("Oops", "Angkanya kebesaran, coba kecilkan input.")
        return
    total_bunga = fv - pv  #Total Bunga = FV - PV


    label_fv.config(text="Future Value: " + rupiah(fv))
    label_bunga.config(text="Total Bunga: " + rupiah(total_bunga))


    #Catatan untuk bunga 0% atau negatif
    if bunga == 0:
        label_info.config(text="Bunga 0%, jadi tidak ada bunga yang diperoleh.")
    elif bunga < 0:
        label_info.config(text="Bunga negatif, nilai uang bisa turun.")
    else:
        label_info.config(text="")


    label_rincian.config(
        text=f"Rumus: FV = PV x (1 + r/n) ^ (n x t)\n\n"
             f"PV = {rupiah(pv)}\nr = {bunga}% = {r}\nn = {n}x setahun\nt = {t} tahun\n\n"
             f"FV = {rupiah(pv)} x (1 + {r}/{n}) ^ ({n} x {t})\nFV = {rupiah(fv)}"
    )


def reset():
    for e in (entry_pv, entry_bunga, entry_waktu):
        e.delete(0, "end")
    combo.current(0)
    label_fv.config(text="Future Value: -")
    label_bunga.config(text="Total Bunga: -")
    label_info.config(text="")
    label_rincian.config(text="")


#Layout
root = tk.Tk()
root.title("Future Value Forecaster")
root.geometry("480x760")
root.configure(bg=BUTTER)
root.resizable(False, False)


#Header
header = tk.Frame(root, bg=TEAL)
header.pack(fill="x")
tk.Label(header, text="Future Value Forecaster", bg=TEAL, fg="white",
         font=(FONT, 18, "bold")).pack(pady=(15, 0))
tk.Label(header, text="Hitung nilai uangmu di masa depan", bg=TEAL, fg=BUTTER,
         font=(FONT, 10)).pack(pady=(0, 15))


#Form input
form = tk.Frame(root, bg=BUTTER)
form.pack(fill="x", padx=30, pady=(15, 0))


def buat_input(teks):
    tk.Label(form, text=teks, bg=BUTTER, fg=GELAP, font=(FONT, 10),
             anchor="w").pack(fill="x", pady=(8, 2))
    entry = tk.Entry(form, font=(FONT, 11), relief="solid", bd=1)
    entry.pack(fill="x", ipady=4)
    return entry


entry_pv = buat_input("Uang saat ini / PV (Rp)")
entry_bunga = buat_input("Bunga tahunan (%)")
entry_waktu = buat_input("Jangka waktu (tahun)")


tk.Label(form, text="Frekuensi bunga", bg=BUTTER, fg=GELAP, font=(FONT, 10),
         anchor="w").pack(fill="x", pady=(8, 2))
combo = ttk.Combobox(form, values=list(FREKUENSI.keys()), state="readonly",
                     font=(FONT, 10))
combo.current(0)
combo.pack(fill="x", ipady=3)


#Tombol
tombol = tk.Frame(root, bg=BUTTER)
tombol.pack(fill="x", padx=30, pady=15)
tk.Button(tombol, text="Hitung Future Value", command=hitung, bg=TEAL, fg="white",
          font=(FONT, 10, "bold"), relief="flat", pady=8, cursor="hand2"
          ).pack(side="left", expand=True, fill="x", padx=(0, 5))
tk.Button(tombol, text="Reset", command=reset, bg="white", fg=TEAL,
          font=(FONT, 10, "bold"), relief="solid", bd=1, pady=8, cursor="hand2"
          ).pack(side="left", expand=True, fill="x", padx=(5, 0))


#Hasil
hasil = tk.Frame(root, bg="white", highlightbackground=TEAL, highlightthickness=2)
hasil.pack(fill="x", padx=30)
label_fv = tk.Label(hasil, text="Future Value: -", bg="white", fg=GELAP,
                    font=(FONT, 12, "bold"), anchor="w")
label_fv.pack(fill="x", padx=12, pady=(10, 2))
label_bunga = tk.Label(hasil, text="Total Bunga: -", bg="white", fg=GELAP,
                       font=(FONT, 12, "bold"), anchor="w")
label_bunga.pack(fill="x", padx=12)
label_info = tk.Label(hasil, text="", bg="white", fg="#B03A2E", font=(FONT, 9, "italic"),
                      anchor="w", wraplength=380, justify="left")
label_info.pack(fill="x", padx=12, pady=(2, 10))


#Detail
label_rincian = tk.Label(root, text="", bg=BUTTER, fg=GELAP, font=(FONT, 9),
                         justify="left", anchor="w")
label_rincian.pack(fill="x", padx=30, pady=15)


root.mainloop()
