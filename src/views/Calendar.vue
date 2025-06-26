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

// カレンダーの属性データ
const attributes = [
  {
    key: "successes",
    dates: ["2025-07-20", "2025-08-11"],
    customData: { type: "holiday" },
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
    customData: { type: "event" },
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
  const dateStr = `${yyyy}${mm}${dd}`;
  router.push(`/reports/show/${dateStr}`);
}

const enemy_hp = ref(100); // 敵のHPの値をここで管理
const user_level = 1; // 1~15の間でユーザーレベルを設定（仮の値、実際はAPI等から取得）

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
