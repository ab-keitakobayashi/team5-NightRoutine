<template>
  <v-row>
    <v-col cols="6" class="text-center">
      <vc-calendar
        @dayclick="ondayClick"
        expanded
        :attributes="attributes"
        class="bg-grey-lighten-1"
      />
    </v-col>
    <v-col cols="6" class="text-center">
      <v-card class="pa-5 bg-grey-lighten-1">
        <v-row>
          <v-col cols="4">
            <v-img :src="`/assets/avatars/${user_level}.png`"></v-img>
            <p class="text-h5 mt-5">{{ user_name }}</p>
          </v-col>
          <v-col cols="8">
            <v-card-title class="text-h3 px-5 text-wrap"
              >Lv.{{ user_level }}</v-card-title
            >
            <v-card-text class="pa-0">選択したEF</v-card-text>
            <v-card-text class="pa-0">選択したEF</v-card-text>
            <v-card-text class="pa-0">選択したEF</v-card-text>
            <v-card-text class="pa-0">選択したEF</v-card-text>
            <v-card-text class="pa-0">選択したEF</v-card-text>
            <v-card-text class="pa-0">次のレベルまで</v-card-text>
          </v-col>
        </v-row>
      </v-card>
    </v-col>
  </v-row>
  <div class="game" :class="{ 'effect-active': isEffect }">
    <v-sheet
      elevation="0"
      color="transparent"
      class="hp-label-sheet"
      style="position: absolute; top: 12px; left: 20px; z-index: 10"
    >
      <span class="hp-label-text text-h5 font-weight-bold"
        >オロチHP: {{ enemy_hp }}</span
      >
    </v-sheet>
    <video src="/assets/game_bg.mp4" autoplay loop muted></video>
    <img class="orochi-left" src="/assets/orochi.png" />
    <img class="knight" :src="`/assets/avatars/${user_level}.png`" />
    <img class="effect" src="/assets/effect.gif" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from "vue";
import axios from "axios";

const userID = ref<String | null>(null); // localStorageから取得
const user_name = ref("");

onMounted(async () => {
  userID.value = String(localStorage.getItem("user_id"));
  try {
    const res = await axios.get(`http://127.0.0.1:8000/user/${userID.value}`);
    user_name.value = res.data.name; // APIのレスポンスに合わせてプロパティ名を指定
    processReports(reports);
    console.log("APIレスポンス", res.data);
  } catch (e) {
    user_name.value = "ニックネーム取得失敗";
    console.log("APIエラー", e);
  }
});

// カレンダーの属性データ
const attributes = [
  {
    key: "successes",
    dates: ["2025-07-20", "2025-08-11"],
    highlight: {
      style: {
        backgroundColor: "red",
        color: "white",
      },
    },
  },
  {
    key: "failures",
    dates: ["2025-07-25"],
    highlight: {
      style: {
        backgroundColor: "blue",
        color: "white",
      },
    },
  },
];

const selectedDate = ref<Date | null>(null);

import { useRouter } from "vue-router";

const router = useRouter();

// 日付がクリックされたらyyyymmdd形式でリンクを生成し遷移
function ondayClick(day: { date: Date }) {
  selectedDate.value = day.date;
  const yyyy = day.date.getFullYear();
  const mm = String(day.date.getMonth() + 1).padStart(2, "0");
  const dd = String(day.date.getDate()).padStart(2, "0");
  const dateStr = `${yyyy}-${mm}-${dd}`;
  router.push(`/reports/show/${dateStr}`);
}

const enemy_hp = ref(100); // 敵のHPの値をここで管理
const user_level = ref(1); // 1~15の間でユーザーレベルを設定（仮の値、実際はAPI等から取得）

const isEffect = ref(false);

// アニメーション周期（CSSのanimation-durationと合わせる）
const ANIMATION_DURATION = 2000; // ms

let intervalId: number | undefined;

onMounted(() => {
  intervalId = window.setInterval(() => {
    // アニメーションの進行度（0～1）
    const now = Date.now() % ANIMATION_DURATION;
    const progress = now / ANIMATION_DURATION;

    // 30%～70%の間だけeffect表示
    if (progress >= 0.3 && progress <= 0.7) {
      if (!isEffect.value) isEffect.value = true;
    } else {
      if (isEffect.value) isEffect.value = false;
    }
  }, 50);
});

onBeforeUnmount(() => {
  if (intervalId) clearInterval(intervalId);
});

//レベルアップ処理

// ダミーデータ（実際はAPI等から取得）
// ここではログイン日数を示す配列を使用
const reports: [string, number][] = [
  ["2025-06-01", 120],
  ["2025-06-02", 150],
  ["2025-06-03", 130],
  ["2025-06-04", 160],
  ["2025-06-05", 140],
  ["2025-06-06", 170],
  ["2025-06-07", 180],
  ["2025-06-08", 200],
  ["2025-06-09", 190],
  ["2025-06-10", 210],
];

// レベルの閾値（指数関数的に設定）
const levelThresholds = [
  1, 1, 2, 4, 7, 12, 20, 34, 57, 95, 158, 262, 435, 723, 1199,
];

// レベルアップ時に呼び出す関数
function announce_level_up(newLevel: number) {
  console.log(`🎉 レベルアップ！新しいレベル: ${newLevel}`);
}

// メイン処理
function processReports(reports: [string, number][]) {
  const loginDays = reports.length;

  // ログイン日数がレベルアップの閾値を超える最大レベルを計算
  let newLevel = 1;
  for (let i = 0; i < levelThresholds.length; i++) {
    if (loginDays >= levelThresholds[i]) {
      newLevel = i + 1;
    } else {
      break;
    }
  }
  user_level.value = newLevel;
  if (newLevel > user_level.value) {
    announce_level_up(newLevel);
  }
}
</script>

<style scoped>
.game {
  position: relative;
  width: 100%;
  height: 320px;
  overflow: hidden;
  background: black;
}

.game video {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  z-index: 1;
}

/* 左側 orochi */
.game .orochi-left {
  position: absolute;
  /* 最初は左5%、アニメーションで右15%まで移動 */
  left: 5%;
  bottom: 10%;
  width: 120px;
  height: auto;
  z-index: 2;
  animation: orochi-left-move 2s infinite alternate ease-in-out;
}

/* 右側 knight */
.game .knight {
  position: absolute;
  /* 最初は右5%、アニメーションで左15%まで移動 */
  right: 5%;
  bottom: 10%;
  width: 120px;
  height: auto;
  z-index: 2;
  animation: knight-move 2s infinite alternate ease-in-out;
}

/* effect（初期は非表示） */
.game .effect {
  position: absolute;
  /* 重なる場所に配置 */
  left: 25%;
  bottom: 10%;
  width: 140px;
  height: auto;
  z-index: 3;
  transform: translateX(-50%);
  display: none;
  pointer-events: none;
}

/* 近づいた時にeffectを表示 */
.game.effect-active .effect {
  display: block;
}

/* アニメーション */
@keyframes orochi-left-move {
  0% {
    left: 5%;
  }
  25% {
    left: 10%; /* 右側 orochiと重なる位置 */
  }
  75% {
    left: 15%; /* 右側 orochiと重なる位置 */
  }
  100% {
    left: 10%; /* 右側 orochiと重なる位置 */
  }
}
@keyframes knight-move {
  0% {
    right: 45%;
  }
  25% {
    right: 65%; /* 左側 orochiと重なる位置 */
  }
  75% {
    right: 55%; /* 左側 orochiと重なる位置 */
  }
  100% {
    right: 65%; /* 左側 orochiと重なる位置 */
  }
}
</style>
