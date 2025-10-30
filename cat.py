import random
import time

fires = ["주방", "전기 콘센트", "쓰레기통", "촛불", "캠핑장"]
tips = {
    "주방": "요리할 때 자리를 비우면 안돼냥!",
    "전기 콘센트": "코드 여러 개 꽂으면 위험하다냥!",
    "쓰레기통": "유리병이 햇빛에 반사되면 불날 수 있다냥!",
    "촛불": "촛불은 꺼지지 않으면 위험하다냥!",
    "캠핑장": "모닥불은 꼭 꺼지고 확인하라냥!"
}

print("🐾🐾🐾 불이야냥! 🧯🐱")
print("귀여운 소방냥이 '호냥'과 함께 불을 꺼보자냥!\n")

fire = random.choice(fires)
print(f"🔥 {fire}에서 불이 났다냥!! 어서 가자냥!!")

time.sleep(1)
success = 0

for i in range(3):
    hit = input("💧 물풍선을 던질까요? (y/n): ")
    if hit.lower() == "y":
        print("💦 불이 조금씩 약해진다냥!")
        success += 1
    else:
        print("🔥 불이 커지고 있다냥!! 조심하라냥!")

time.sleep(1)
if success >= 2:
    print("\n🎉 불이 완전히 꺼졌다냥!")
else:
    print("\n😭 아깝다냥! 불이 완전히 꺼지진 않았지만, 다음엔 더 잘할거다냥!")

print(f"\n🐾 원인은 '{fire}' 때문이래냥.")
print("📘 예방법:", tips[fire])

time.sleep(1)
print("\n✨ 오늘도 마을이 조금 더 안전해졌다냥!")
