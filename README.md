# TTS-Indonesia-Gratis

![Screen Shot 2024-07-23 at 3 20 33 AM](https://github.com/user-attachments/assets/2eac1c9e-3621-43ea-b86b-c87c72883995)

Aplikasi ini digunakan untuk menghasilkan suara berbasis teks dengan berbagai pilihan pembicara. Teknologi yang digunakan meliputi model text-to-speech (TTS) yang canggih dengan konversi teks ke fonem (G2P). Model ini dilatih khusus untuk bahasa Indonesia, Jawa, dan Sunda.

## Data

- [Indonesian Azure TTS](https://depia.wiki/files/azure-tts.tar)

## Fitur

- Menghasilkan suara dari teks dalam berbagai bahasa dan aksen.
- Pilihan pembicara yang beragam dengan karakter suara yang unik.
- Antarmuka pengguna yang interaktif dan mudah digunakan dengan Gradio.
- Tema khusus dengan gradasi warna kuning ke putih.

## Pembicara yang Tersedia
![ardi](https://github.com/user-attachments/assets/d0b82dea-7b14-4347-91f5-27574d3bcbb1)
![gadis](https://github.com/user-attachments/assets/b016cccb-7f7c-4643-8551-597fd56252bb)
![wibowo](https://github.com/user-attachments/assets/26e29e38-c364-4bbb-b71f-028c7dfeccd1)

- **Wibowo**: Suara jantan berwibawa
- **Ardi**: Suara lembut dan hangat
- **Gadis**: Suara perempuan yang merdu
- **Juminten**: Suara perempuan jawa (bahasa jawa)
- **Asep**: Suara lelaki sunda (bahasa sunda)

## Cara Menggunakan

1. Masukkan teks yang ingin diubah menjadi suara.
2. Pilih kecepatan bicara yang diinginkan.
3. Pilih bahasa dan pembicara yang diinginkan.
4. Klik tombol "Lakukan Inferensi Audio" untuk menghasilkan suara.

## Contoh Suara


https://github.com/user-attachments/assets/905c4d71-686d-4270-a6dd-f134fa8dbefc


https://github.com/user-attachments/assets/a0d2089b-4a92-4eb4-8f1f-02b60294ce93


https://github.com/user-attachments/assets/3601206d-3a9f-41cc-ab7a-2c36bdbbd359


https://github.com/user-attachments/assets/ce1730e2-340b-41ea-b436-d691328a07af



- [Wibowo](audio_samples/wibowo.wav)
- [Gadis](audio_samples/gadis.wav)
- [Juminten (Jawa)](audio_samples/juminten_jawa.wav)
- [Asep (Sunda)](audio_samples/asep_sunda.wav)

## Teknologi yang Digunakan

- [Gradio](https://gradio.app/) untuk antarmuka pengguna
- [G2P](https://github.com/kaldi-asr/g2p-seq2seq) untuk konversi teks ke fonem
- Model TTS yang dilatih khusus untuk bahasa Indonesia, Jawa, dan Sunda

# Unduh Model TTS Bahasa Indonesia

File Model dapat diunduh di : [Releases](https://github.com/Wikidepia/indonesian-tts/releases/) tab.

**DO NOT USE FOR COMMERCIAL PURPOSES!**

## Model changelog

### v1.2 (Aug 12, 2022)

Finetuned from v1.1 model on:

- 4 hours of Audiobook dataset
- 2000 sample of Azure TTS
- High quality TTS data for Javanese & Sundanese

### v1.1 (Aug 6, 2022)

Finetuned from LJSpeech model on:

- 4 hours of Audiobook dataset
- 2000 sample of Azure TTS

### v1.0 (Jun 23, 2022)

Trained from scratch on:

- 4 hours of Audiobook dataset.

## Lisensi

Proyek ini dilisensikan di bawah lisensi MIT. Lihat file [LICENSE](LICENSE) untuk informasi lebih lanjut.

## Kontribusi

Kami menyambut kontribusi dari siapa pun. Untuk berkontribusi, silakan buat _pull request_ atau buka _issue_ untuk mendiskusikan perubahan yang ingin Anda lakukan.

## Kontak

Untuk informasi lebih lanjut, silakan hubungi __drat di [email@example.com](mailto:email@example.com).

---

Energi Semesta Digital © 2024 __drat. | 🇮🇩 Untuk Indonesia Jaya!
