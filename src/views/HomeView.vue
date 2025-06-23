<template>
  <v-row>
    <v-col cols="4">
      <!-- 開始時間、終了時間 -->
      <v-row>
        <v-col cols="6">
          <p>開始時間</p>
          <v-text-field
            v-model="startTime"
            placeholder="例: 08:00"
            type="time"
          ></v-text-field>
        </v-col>
        <v-col cols="6">
          <p>終了時間</p>
          <v-text-field
            v-model="endTime"
            placeholder="例: 08:00"
            type="time"
          ></v-text-field>
        </v-col>
        <v-row>
          <template v-for="(time, idx) in timeSlots" :key="time">
            <v-col cols="3">
              <div class="d-flex align-center justify-center fill-height">
                <p>{{ time }}~</p>
              </div>
            </v-col>
            <v-col cols="9">
              <v-text-field
                v-model="tasks[idx]"
                placeholder="議事録作成"
                type="text"
              ></v-text-field>
            </v-col>
          </template>
        </v-row>
      </v-row>
    </v-col>
    <v-col cols="4">
      <v-card>
        <v-card-title class="text-h5">testttttttttttttttttttt</v-card-title>
        <v-card-text>
          <p>test</p>
        </v-card-text>
      </v-card>
    </v-col>
    <v-col cols="4">
      <v-card>
        <v-card-title class="text-h5">testtttttttttttttttttt</v-card-title>
        <v-card-text>
          <p>test</p>
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</template>

<script setup>
import { ref, computed, watch } from "vue";

// 時刻入力用
const startTime = ref("09:00");
const endTime = ref("11:00");

// タスク内容
const tasks = ref([]);

// 30分ごとの時刻リストを生成
const timeSlots = computed(() => {
  if (!startTime.value || !endTime.value) return [];
  const result = [];
  let [sh, sm] = startTime.value.split(":").map(Number);
  let [eh, em] = endTime.value.split(":").map(Number);
  let start = sh * 60 + sm;
  let end = eh * 60 + em;
  while (start < end) {
    const h = String(Math.floor(start / 60)).padStart(2, "0");
    const m = String(start % 60).padStart(2, "0");
    result.push(`${h}:${m}`);
    start += 30;
  }
  // tasks配列の長さを調整
  if (tasks.value.length !== result.length) {
    tasks.value = Array(result.length).fill("");
  }
  return result;
});

// tasks配列の長さを自動調整
watch(timeSlots, (slots) => {
  if (tasks.value.length !== slots.length) {
    tasks.value = Array(slots.length).fill("");
  }
});
</script>
