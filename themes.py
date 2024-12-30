"""
████████╗████████╗███████╗                                                          
╚══██╔══╝╚══██╔══╝██╔════╝                                                          
   ██║      ██║   ███████╗                                                          
   ██║      ██║   ╚════██║                                                          
   ██║      ██║   ███████║                                                          
   ╚═╝      ╚═╝   ╚══════╝                                                          
██╗███╗   ██╗██████╗  ██████╗ ███╗   ██╗███████╗███████╗██╗ █████╗ ██╗  ██╗██╗   ██╗
██║████╗  ██║██╔══██╗██╔═══██╗████╗  ██║██╔════╝██╔════╝██║██╔══██╗██║ ██╔╝██║   ██║
██║██╔██╗ ██║██║  ██║██║   ██║██╔██╗ ██║█████╗  ███████╗██║███████║█████╔╝ ██║   ██║
██║██║╚██╗██║██║  ██║██║   ██║██║╚██╗██║██╔══╝  ╚════██║██║██╔══██║██╔═██╗ ██║   ██║
██║██║ ╚████║██████╔╝╚██████╔╝██║ ╚████║███████╗███████║██║██║  ██║██║  ██╗╚██████╔╝
╚═╝╚═╝  ╚═══╝╚═════╝  ╚═════╝ ╚═╝  ╚═══╝╚══════╝╚══════╝╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ 
                                                                                    
Script ini dibuat oleh __drat

Petunjuk:
1. Script ini digunakan untuk menghasilkan suara berbasis teks dengan berbagai pilihan pembicara.
2. Teknologi yang digunakan meliputi model text-to-speech (TTS) yang canggih dengan konversi teks ke fonem (G2P).
3. Model yang dipakai dilatih khusus untuk bahasa Indonesia, Jawa, dan Sunda.
4. Antarmuka dibuat dengan menggunakan Gradio dengan tema kustom bernama MetafisikTheme.

Cara Menggunakan:
1. Masukkan teks yang ingin diubah menjadi suara.
2. Pilih kecepatan bicara yang diinginkan.
3. Pilih bahasa dan pembicara yang diinginkan.
4. Klik tombol "Lakukan Inferensi Audio" untuk menghasilkan suara.
"""

from __future__ import annotations
from typing import Iterable
from gradio.themes.base import Base
from gradio.themes.utils import colors, fonts, sizes

class MetafisikTheme(Base):
    def __init__(
        self,
        *,
        primary_hue: colors.Color | str = colors.orange,
        secondary_hue: colors.Color | str = colors.yellow,
        neutral_hue: colors.Color | str = colors.gray,
        spacing_size: sizes.Size | str = sizes.spacing_md,
        radius_size: sizes.Size | str = sizes.radius_md,
        text_size: sizes.Size | str = sizes.text_lg,
        font: fonts.Font
        | str
        | Iterable[fonts.Font | str] = (
            fonts.GoogleFont("Quicksand"),
            "ui-sans-serif",
            "sans-serif",
        ),
        font_mono: fonts.Font
        | str
        | Iterable[fonts.Font | str] = (
            fonts.GoogleFont("IBM Plex Mono"),
            "ui-monospace",
            "monospace",
        ),
    ):
        super().__init__(
            primary_hue=primary_hue,
            secondary_hue=secondary_hue,
            neutral_hue=neutral_hue,
            spacing_size=spacing_size,
            radius_size=radius_size,
            text_size=text_size,
            font=font,
            font_mono=font_mono,
        )
        super().set(
            body_background_fill="linear-gradient(to bottom, #FFFFE0, #FFFFFF)",  # Gradient from light yellow to white
            body_background_fill_dark="linear-gradient(to bottom, #FFFFE0, #FFFFFF)",  # Same gradient for dark mode
            button_primary_background_fill="linear-gradient(90deg, #FFA500, #FF4500)",  # Orange to dark orange gradient
            button_primary_background_fill_hover="linear-gradient(90deg, #FFB347, #FF6347)",  # Lighter orange gradient
            button_primary_text_color="white",
            button_primary_background_fill_dark="linear-gradient(90deg, #FF8C00, #FF4500)",  # Darker orange gradient
            slider_color="*secondary_300",
            slider_color_dark="*secondary_600",
            block_title_text_weight="600",
            block_border_width="3px",
            block_shadow="*shadow_drop_lg",
            button_primary_shadow="*shadow_drop_lg",
            button_large_padding="32px",
        )
