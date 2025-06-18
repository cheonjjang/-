import streamlit as st
import random
import math

number_counts = {
    1: 19, 2: 14, 3: 29, 4: 17, 5: 17, 6: 33, 7: 32, 8: 20, 9: 23,
    10: 17, 11: 28, 12: 31, 13: 27, 14: 28, 15: 24, 16: 26, 17: 22,
    18: 24, 19: 28, 20: 25, 21: 27, 22: 25, 23: 18, 24: 24, 25: 17,
    26: 26, 27: 23, 28: 22, 29: 25, 30: 31, 31: 23, 32: 26, 33: 28,
    34: 28, 35: 32, 36: 22, 37: 25, 38: 30, 39: 19, 40: 24, 41: 18,
    42: 21, 43: 14, 44: 23, 45: 31
}

numbers = list(number_counts.keys())
total_counts = sum(number_counts.values())
mean_count = total_counts / len(numbers)

raw_weights = []
for n in numbers:
    base_weight = number_counts[n] / total_counts
    if number_counts[n] < mean_count * 0.8:
        base_weight *= 1.2
    raw_weights.append(base_weight)

corrected_weights = [math.sqrt(w) for w in raw_weights]
sum_weights = sum(corrected_weights)
final_weights = [w / sum_weights for w in corrected_weights]

st.title("🤖 AI 로또 추첨기 최적화버전")

num_sets = st.slider("추천 세트 수:", 1, 5, 1)

all_results = []

if st.button("📩 번호 추천 받기"):
    for set_num in range(num_sets):
        attempt = 0
        while True:
            attempt += 1
            selected_numbers = []
            available_numbers = numbers.copy()
            available_weights = final_weights.copy()

            for _ in range(6):
                selected = random.choices(available_numbers, weights=available_weights, k=1)[0]
                selected_numbers.append(selected)
                idx = available_numbers.index(selected)
                del available_numbers[idx]
                del available_weights[idx]

            selected_numbers.sort()

            odds = sum(1 for n in selected_numbers if n % 2 == 1)
            lows = sum(1 for n in selected_numbers if n <= 22)
            if (odds in [2,3,4]) and (lows in [2,3,4]):
                break
            if attempt > 100:
                break

        all_results.append(selected_numbers)

        st.write(f"### 🎯 추천 세트 {set_num+1}")
        cols = st.columns(6)
        for i in range(6):
            cols[i].markdown(
                f"<div style='background-color:#FFD700;border-radius:50%;width:80px;height:80px;display:flex;justify-content:center;align-items:center;font-size:30px;font-weight:bold;'>{selected_numbers[i]}</div>",
                unsafe_allow_html=True
            )

    # 복사용 텍스트 생성
    result_text = ""
    for idx, nums in enumerate(all_results):
        result_text += f"세트 {idx+1}: {', '.join(str(n) for n in nums)}\n"

    st.text_area("📋 복사해서 카톡에 붙여넣기:", value=result_text, height=150)
