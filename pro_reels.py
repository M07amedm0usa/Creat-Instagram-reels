import asyncio
import edge_tts
import os
import subprocess

# --- الإعدادات (تقدر تغير النص هنا للتجربة) ---
TEXT = "يا أهلاً بيك يا بطل.. ده أول فيديو ريل يتعمل بالكامل أوتوماتيك بصوت شاكر المصري من جوه جيت هاب أكشنز! الأتمتة هي المستقبل."
VOICE = "ar-EG-ShakirNeural"
OUTPUT_AUDIO = "audio.mp3"
OUTPUT_VIDEO = "final_reel.mp4"

async def generate_audio():
    if not os.path.exists("audio"): os.makedirs("audio", exist_ok=True)
    communicate = edge_tts.Communicate(TEXT, VOICE)
    await communicate.save(OUTPUT_AUDIO)
    print("✅ تم توليد الصوت بنجاح.")

def generate_video():
    # بنشوف لو فيه صور في فولدر assets
    assets_dir = "assets"
    images = sorted([f for f in os.listdir(assets_dir) if f.endswith(('.png', '.jpg'))])
    
    if len(images) == 0:
        print("❌ مفيش صور! هحاول أدور على فيديو خلفية..")
        # هنا ممكن نطورها مستقبلاً لجبر الخواطر بفيديو افتراضي
        return

    # أمر FFmpeg: دمج الصور مع الصوت وعمل زووم بسيط (Ken Burns Effect)
    # ملاحظة: هيفترض إن مدة الفيديو هي مدة ملف الصوت أوتوماتيك
    cmd = (
        f"ffmpeg -loop 1 -i assets/{images[0]} -i {OUTPUT_AUDIO} "
        f"-vf 'zoompan=z=\"min(zoom+0.0015,1.5)\":d=750:s=1080x1920,format=yuv420p' "
        f"-c:v libx264 -c:a aac -shortest {OUTPUT_VIDEO} -y"
    )
    
    print("🎬 جاري رندرة الفيديو...")
    subprocess.run(cmd, shell=True)
    print(f"✨ تم إنتاج الفيديو بنجاح: {OUTPUT_VIDEO}")

if __name__ == "__main__":
    asyncio.run(generate_audio())
    generate_video()
      
