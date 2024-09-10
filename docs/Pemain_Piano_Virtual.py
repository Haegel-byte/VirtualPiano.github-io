import cv2
import numpy as np
import pygame
import os
import random

# Fungsi untuk mencari folder suara
def cari_folder_suara():
    kemungkinan_lokasi = [
        '17749__jaz_the_man_2__do-re-mi-fa-so-la-ti-do',
        os.path.join('..', '17749__jaz_the_man_2__do-re-mi-fa-so-la-ti-do'),
        os.path.join(os.path.dirname(__file__), '17749__jaz_the_man_2__do-re-mi-fa-so-la-ti-do')
    ]
    
    for lokasi in kemungkinan_lokasi:
        if os.path.exists(lokasi):
            wav_files = [f for f in os.listdir(lokasi) if f.endswith('.wav')]
            if wav_files:
                return lokasi
    
    raise FileNotFoundError("Folder suara dengan file WAV tidak ditemukan")

# Fungsi untuk mencetak isi folder
def cetak_isi_folder(folder):
    print(f"Isi folder {folder}:")
    for item in os.listdir(folder):
        print(f"- {item}")

# Cari folder suara
try:
    suara_folder = cari_folder_suara()
    print(f"Folder suara ditemukan: {suara_folder}")
    cetak_isi_folder(suara_folder)
except FileNotFoundError as e:
    print(f"Error: {e}")
    print("Pastikan folder suara berada di lokasi yang benar dan berisi file WAV.")
    exit(1)

# Inisialisasi pygame untuk audio
pygame.init()
pygame.mixer.init()

# Muat suara piano
suara_piano = {}
for file in os.listdir(suara_folder):
    if file.endswith('.wav'):
        nada = file.split('__')[-1].split('.')[0].lower()
        file_path = os.path.join(suara_folder, file)
        suara_piano[nada] = pygame.mixer.Sound(file_path)
        print(f"Berhasil memuat: {file}")

if not suara_piano:
    print("Tidak ada file suara yang ditemukan. Program akan berhenti.")
    exit(1)

# Ubah dictionary tombol_ke_nada
tombol_ke_nada = {
    pygame.K_q: 'do',
    pygame.K_w: 're',
    pygame.K_e: 'mi',
    pygame.K_r: 'fa',
    pygame.K_t: 'sol',
    pygame.K_y: 'la',
    pygame.K_u: 'si',
    pygame.K_i: 'do-octave',
    pygame.K_o: 're-stretched',
    pygame.K_p: 'mi-stretched',
    pygame.K_f: 'fa-stretched',
    pygame.K_g: 'sol-stretched',
    pygame.K_h: 'la-stretched',
    pygame.K_j: 'si-stretched',
    pygame.K_k: 'do-stretched',
    pygame.K_l: 'do-stretched-octave'
}

# Konstanta untuk UI
LEBAR_LAYAR = 1000
TINGGI_LAYAR = 400
WARNA_LATAR = (50, 50, 50)
WARNA_TUTS_PUTIH = (255, 255, 255)
WARNA_TUTS_HITAM = (0, 0, 0)
WARNA_TEKS = (200, 200, 200)
WARNA_EFEK = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]
tuts_width = LEBAR_LAYAR // len(tombol_ke_nada)

# Buat jendela Pygame
layar = pygame.display.set_mode((LEBAR_LAYAR, TINGGI_LAYAR))
pygame.display.set_caption('Piano Virtual')

# Font untuk teks
font_kecil = pygame.font.Font(None, 24)
font_besar = pygame.font.Font(None, 36)

class AnimeCharacter:
    def __init__(self):
        self.states = {
            'diam': self.load_frames(['diam1.png', 'diam2.png', 'diam3.png', 'diam4.png']),
            'bahagia': self.load_frames(['bahagia1.png', 'bahagia2.png', 'bahagia3.png'])
        }
        self.current_state = 'diam'
        self.current_frame = 0
        self.animation_speed = 30
        self.tick_count = 0
        self.state_duration = 60
        self.is_playing = False

    def load_frames(self, file_names):
        frames = []
        for file in file_names:
            frame_path = os.path.join('character', file)
            frame = pygame.image.load(frame_path).convert_alpha()
            frame = pygame.transform.scale(frame, (200, 300))
            frames.append(frame)
        return frames

    def update(self):
        if self.is_playing:
            self.tick_count += 1
            if self.tick_count >= self.animation_speed:
                self.current_frame = (self.current_frame + 1) % len(self.states[self.current_state])
                self.tick_count = 0
            
            if self.current_state == 'bahagia' and self.tick_count >= self.state_duration:
                self.set_state('diam')
        else:
            self.current_frame = 0  # Kembali ke frame pertama saat tidak bermain

    def draw(self, surface):
        frame = self.states[self.current_state][self.current_frame]
        x = 20
        y = surface.get_height() - frame.get_height() - 10
        surface.blit(frame, (x, y))

    def set_state(self, state):
        if state in self.states and state != self.current_state:
            self.current_state = state
            self.current_frame = 0
            self.tick_count = 0

    def start_playing(self):
        self.is_playing = True
        self.set_state('bahagia')

    def stop_playing(self):
        self.is_playing = False
        self.set_state('diam')

anime_character = AnimeCharacter()
print(f"Jumlah frame diam: {len(anime_character.states['diam'])}")
print(f"Jumlah frame bahagia: {len(anime_character.states['bahagia'])}")

print(f"Folder karakter: {os.path.join('character')}")
print(f"Jumlah frame diam: {len(anime_character.states['diam'])}")
print(f"Jumlah frame bahagia: {len(anime_character.states['bahagia'])}")

def gambar_tuts(tombol_aktif=None):
    piano_width = LEBAR_LAYAR - 250  # Mengurangi lebar piano untuk memberi ruang karakter
    tuts_width = piano_width // len(tombol_ke_nada)
    for i, (tombol, nada) in enumerate(tombol_ke_nada.items()):
        x = 250 + i * tuts_width  # Memulai piano dari posisi x = 250
        warna = WARNA_TUTS_PUTIH if i % 2 == 0 else WARNA_TUTS_HITAM
        if tombol == tombol_aktif:
            warna = (150, 150, 150)  # Warna saat tombol ditekan
        pygame.draw.rect(layar, warna, (x, 100, tuts_width - 1, 250))
        pygame.draw.rect(layar, WARNA_TEKS, (x, 100, tuts_width - 1, 250), 2)
        
        teks_tombol = font_kecil.render(pygame.key.name(tombol).upper(), True, WARNA_TEKS)
        teks_nada = font_besar.render(nada, True, WARNA_TEKS)
        layar.blit(teks_tombol, (x + tuts_width//2 - teks_tombol.get_width()//2, 320))
        layar.blit(teks_nada, (x + tuts_width//2 - teks_nada.get_width()//2, 110))

class NoteEffect:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.radius = 5
        self.max_radius = 30
        self.life = 30
        self.expanding = True

    def update(self):
        if self.expanding:
            self.radius += 1
            if self.radius >= self.max_radius:
                self.expanding = False
        else:
            self.radius -= 1
        self.life -= 1

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.radius), 2)

note_effects = []

def draw_note_hint(surface, note):
    hint_text = font_kecil.render(f"Nada: {note}", True, WARNA_TEKS)
    surface.blit(hint_text, (LEBAR_LAYAR // 2 - hint_text.get_width() // 2, 50))

berjalan = True
tombol_aktif = None
while berjalan:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            berjalan = False
        elif event.type == pygame.KEYDOWN:
            if event.key in tombol_ke_nada:
                nada = tombol_ke_nada[event.key]
                suara_piano[nada].play()
                print(f"Memainkan nada: {nada}")
                tombol_aktif = event.key
                anime_character.start_playing()
                x = 250 + list(tombol_ke_nada.keys()).index(event.key) * (LEBAR_LAYAR - 250) // len(tombol_ke_nada)
                note_effects.append(NoteEffect(x + (LEBAR_LAYAR - 250) // len(tombol_ke_nada) // 2, 225, random.choice(WARNA_EFEK)))
        elif event.type == pygame.KEYUP:
            if event.key in tombol_ke_nada:
                tombol_aktif = None
                anime_character.stop_playing()

    layar.fill(WARNA_LATAR)
    
    gambar_tuts(tombol_aktif)
    
    judul = font_besar.render("Piano Virtual", True, WARNA_TEKS)
    layar.blit(judul, (LEBAR_LAYAR//2 - judul.get_width()//2, 10))
    
    for effect in note_effects[:]:
        effect.update()
        effect.draw(layar)
        if effect.life <= 0:
            note_effects.remove(effect)
    
    anime_character.update()
    anime_character.draw(layar)
    
    if tombol_aktif:
        draw_note_hint(layar, tombol_ke_nada[tombol_aktif])
    
    pygame.display.flip()

pygame.quit()

