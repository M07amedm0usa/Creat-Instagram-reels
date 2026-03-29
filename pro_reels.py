import asyncio
import edge_tts
import os
import subprocess

# --- الإعدادات ---
# النص اللي شاكر هينطقه
TEXT = "أهلاً بيك يا بطل، ده أول فيديو ريل يتعمل بالكامل أوتوماتيك بصوت شاكر المصري من جوه جيت هاب أكشنز! الأتمتة هي المستقبل."
VOICE = "ar-EG-ShakirNeural"
OUTPUT_AUDIO = "audio.mp3"
OUTPUT_VIDEO = "final_reel.mp4"

async def generate_audio():
    if not os.path.exists("audio"): 
        os.makedirs("audio", exist_ok=True)
    
    print(f"🎤 جاري توليد الصوت بصوت {VOICE}...")
    communicate = edge_tts.Communicate(TEXT, VOICE)
    await communicate.save(OUTPUT_AUDIO)
    print("✅ تم توليد الصوت بنجاح.")

def generate_video():
    assets_dir = "assets"
    # البحث عن الصور بكل الصيغ الممكنة (png, jpg, jpeg)
    images = sorted([f for f in os.listdir(assets_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
    
    if len(images) == 0:
        print("❌ خطأ: مفيش صور في فولدر assets!")
        return

    print(f"📸 تم العثور على {len(images)} صور. جاري التحضير...")

    # أمر FFmpeg الاحترافي:
    # 1. بياخد أول صورة (images[0])
    # 2. بيعمل Zoom In تدريجي (zoompan)
    # 3. بيظبط المقاس 1080x1920 (مقاس الريلز)
    # 4. بيخلي مدة الفيديو هي نفس مدة ملف الصوت بالظبط (-shortest)
    
    cmd = (
        f"ffmpeg -loop 1 -i assets/{images[0]} -i {OUTPUT_AUDIO} "
        f"-vf \"zoompan=z='min(zoom+0.0015,1.5)':d=750:s=1080x1920,format=yuv420p\" "
        f"-c:v libx264 -c:a aac -b:a 192k -shortest {OUTPUT_VIDEO} -y"
    )
    
    print("🎬 جاري رندرة الفيديو (Rendering)...")
    result = subprocess.run(cmd, shell=True)
    
    if result.returncode == 0:
        print(f"✨ مبروك! الفيديو جاهز: {OUTPUT_VIDEO}")
    else:
        print("❌ حصلت مشكلة أثناء رندرة الفيديو.")

if __name__ == "__main__":
    # تشغيل توليد الصوت ثم الفيديو
    asyncio.run(generate_audio())
    generate_video()
        
