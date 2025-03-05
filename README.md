# Dicoding Collection Dashboard ✨

Sebelum membuat Dashboard dan mendeploy nya menggunakan streamlit siapkan file-file berikut:
- forlder dashboard yang berisi all_data.csv dan dashboard.py
- data yang berisi: day.csv, hour.csv dan lainnya.
- notebook.ipynb
- requirements.txt

Berikut langkah-langkahnya:

## 1. Membuat Folder di VSCode
```
- Buat folder bernama dashboard yang bdidalamnya berisi all_data.csv
- Buka vscode dan buat file baru bernama dashboard.py
- ketikkan kode program berisi library dan program didalamnya
- Pada terminal, ketikkan "pip freeze > requirements.txt" untuk menginstall semua library yang dipakai.
- lalu lakukan environment pada terminal
```
## 2. Setup Environment - Anaconda
```
Untuk mereview hasil program dashboard.py, ketikkan pada terminal:
cd ~/Desktop
cd dashboard
conda activate streamlit_env
streamlit run dashboard.py

lalu akan diarahkan ke chrome/browse/dll untuk menampilkan hasil program streamlitnya.
```

## 3. Deploy steamlit app
```
Setelah melakukan hal diatas, sekarang untuk mendeploy semua Kode program dan data yang sudah dimiliki.
- Buat repository pada github yang berisi file file dengan struktur:
  submission
  ├───dashboard
  | ├───main_data.csv
  | └───dashboard.py
  ├───data
  | ├───day.csv
  | └───hour.csv
  | └───dan-lainnya.csv
  ├───notebook.ipynb
  ├───README.md
  └───requirements.txt
  └───url.txt (Jika menerapkan saran ketiga)
- Lalu masuk ke website streamlit dan hubungkan akun github dengan akun streamlit.
- Setelah terhubung akan diarahkan ke tampilan dashboar streamlit berisi file-file github
- pilih *create app* di pojok kanan atas
- pilih deploy now
- lalu akan diminta untuk mengisi berupa Repository Github, Branch, Main File Path, dan Up URL. isi sesuai dengan repository yang diinginkan.
- Lalu pili deploy dan akan ditampilkan hasilnya.
```
