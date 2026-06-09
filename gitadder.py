import subprocess
import os

def fast_commit(commit_message="SStudio: Update app, static and requirements"):
    # Biz kuzatadigan fayl va papkalar ro'yxati
    targets = ["app", "static", "requirements.txt"]
    
    # Mavjud bo'lganlarini saralab olamiz
    files_to_add = [t for t in targets if os.path.exists(t)]
    
    if not files_to_add:
        print("Hech qanday nishonli (app, static, requirements) fayl topilmadi!")
        return

    try:
        # 1. Faqat kerakli fayllarni qo'shish
        for target in files_to_add:
            subprocess.run(["git", "add", target], check=True)
            print(f"✅ {target} tayyorlandi.")
        
        # 2. Commit qilish
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        print(f"\n🚀 Muvaffaqiyatli commit qilindi: '{commit_message}'")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Xatolik yuz berdi: {e}")

if __name__ == "__main__":
    fast_commit()