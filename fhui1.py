import subprocess
import os
from datetime import date, timedelta

# GANTI TOKEN INI 
twitter_auth_token = '341ef8ffa60347d7451612e47a35d1fc5374e0f2' 

limit_per_hari = 300

# --- PERUBAHAN KEYWORDS (SENTIMEN KASUS FH UI) ---
keywords = [
    # NETRAL
    "@sampahfhui", "FH UI pelecehan", 
    "grup WA FH UI", "chat mesum FH UI", "kasus FH UI", "BEM FH UI",
    # POSITIF (Membela/Meremehkan)
    "DO pelaku FH UI", "biadab FH UI", "hukum pelaku FH UI", 
    "drop out FH UI", "cowok FH UI sakit", "kasihan korban FH UI", "kawal kasus FH UI",
    # NEGATIF (Mengecam)
    "cuma dark jokes", "jokes tongkrongan", "bocorin chat privasi", 
    "privasi grup", "lebay FH UI", "nama baik FH UI", "jangan pukul rata FH UI"
]

npx_command = "npx.cmd" if os.name == "nt" else "npx"

# --- PERUBAHAN RENTANG WAKTU (10 APRIL - 10 MEI 2026) ---
start_date_global = date(2026, 4, 10)
end_date_global = date(2026, 5, 10)

for keyword in keywords:
    print(f"\n{'='*70}")
    print(f"MEMULAI SCRAPING KATA KUNCI: {keyword.upper()} (MODE HARIAN)")
    print(f"{'='*70}")
    
    # Hapus spasi dan simbol '@' khusus untuk nama file agar tidak error
    safe_filename = keyword.replace(" ", "_").replace("@", "")
    
    current_date = start_date_global
    while current_date <= end_date_global:
        next_date = current_date + timedelta(days=1) 
        
        start_str = current_date.strftime("%Y-%m-%d")
        end_str = next_date.strftime("%Y-%m-%d")
        
        # --- DIPERTAHANKAN DARI KODEMU ---
        # Nama file dibuat dinamis per hari (contoh: FH_UI_pelecehan_2026-04-10.csv)
        filename = f"{safe_filename}_{start_str}.csv"
        # -------------------------
        
        if " " in keyword:
            search_query = f'"{keyword}" since:{start_str} until:{end_str} lang:id'
        else:
            search_query = f'{keyword} since:{start_str} until:{end_str} lang:id'
        
        command = [
            npx_command, "-y", "tweet-harvest@2.6.1",
            "-o", filename,
            "-s", search_query,
            "--tab", "LATEST",
            "-l", str(limit_per_hari),
            "--delay", "7",
            "--token", twitter_auth_token
        ]
        
        print(f"\n--> Tanggal: {start_str} | Target: {limit_per_hari} tweet")
        
        try:
            process = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            print(f"    Sukses ditarik dan disimpan ke {filename}")
        except subprocess.CalledProcessError:
            print(f"    Gagal/Tidak ada data di tanggal {start_str}")
        
        current_date += timedelta(days=1)

print("\n=== SEMUA PROSES HARIAN SELESAI ===")