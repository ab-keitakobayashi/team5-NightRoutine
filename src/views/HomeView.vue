<template>
  <v-row>
    <v-col cols="4">
      <!-- 開始時間、終了時間 -->
      <v-row no-gutters>
        <v-col cols="5">
          <p>開始時間</p>
          <v-text-field
            variant="outlined"
            v-model="startTime"
            placeholder="例: 08:00"
            type="time"
          ></v-text-field>
        </v-col>
        <v-col cols="2"></v-col>
        <v-col cols="5">
          <p>終了時間</p>
          <v-text-field
            variant="outlined"
            v-model="endTime"
            placeholder="例: 08:00"
            type="time"
          ></v-text-field>
        </v-col>
        <v-row>
          <template v-for="(time, idx) in timeSlots" :key="time">
            <v-col cols="3" class="my-0 py-0">
              <div class="d-flex align-center justify-end fill-height">
                <p>{{ time }}~</p>
              </div>
            </v-col>
            <v-col cols="9" class="my-0 py-0">
              <v-text-field
                variant="outlined"
                v-model="tasks[idx]"
                placeholder="議事録作成"
                type="text"
                @blur="autoFillTask(idx)"
              ></v-text-field>
            </v-col>
          </template>
        </v-row>
      </v-row>
    </v-col>
    <v-col cols="4">
      <p>よかったこと</p>
      <v-textarea
        v-model="successes"
        variant="outlined"
        name="successes"
        placeholder="よかったことを記入してください"
        rows="10"
        auto-grow
        outlined
      ></v-textarea>
      <p>改善点</p>
      <v-textarea
        v-model="failures"
        variant="outlined"
        name="failures"
        placeholder="改善点を記入してください"
        rows="10"
        auto-grow
        outlined
      ></v-textarea>
    <v-btn @click="save" class="text-black ma-5"> 一時保存 </v-btn>
    <v-btn v-if="isResubmit" @click="re_submit" class="text-black ma-5">再送信</v-btn>
    <v-btn v-else @click="submit" class="text-black ma-5">送信</v-btn>
    </v-col>
    <v-col cols="4">
      <p>AI評価</p>
      <v-table theme="dark">
        <thead>
          <tr>
            <th>EF項目</th>
            <th>増減ポイント</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, idx) in efData" :key="idx">
            <td>{{ item.EF_item }}</td>
            <td>{{ item.score }}</td>
          </tr>
        </tbody>
      </v-table>
      <p>AIコメント</p>
      <v-textarea
        v-model="assessment"
        bg-color="grey-darken-3"
        variant="outlined"
        name="assessment"
        placeholder="AIがコメントを記入します"
        rows="10"
        auto-grow
        outlined
      ></v-textarea>
    </v-col>
  </v-row>
</template>

<script setup>


import { ref, computed, watch } from "vue";
import axios from "axios";

// 時刻入力用
const startTime = ref("09:00");
const endTime = ref("18:00");
const successes = ref("");
const failures = ref("");
const assessment = ref("");
const item = ref({});
const userID = ref(1); // ユーザーIDのダミー値
// システムの現在の日付を"YYYY-MM-DD"形式で取得
const day = ref(new Date().toISOString().slice(0, 10));

// タスク内容
const tasks = ref([]);
const props = defineProps(['inputdate']);

// 画面表示時とinputdateが変わった時にgetを呼ぶ
console.log(`inputdate: ${props.inputdate}`);

const isResubmit = ref(false);

watch(
  () => props.inputdate,
  (newVal) => {
    if (newVal) {
      get(newVal);
      day.value = props.inputdate;
      isResubmit.value = true; // 再送信ボタンに切り替え
    }
  },
  { immediate: true }
);



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

// 未記入箇所に直前の異なる業務内容を自動記入
function autoFillTask(idx) {
  // idxより前の空欄を埋める
  for (let i = 0; i < idx; i++) {
    if (!tasks.value[i]) {
      // 直前の業務内容を探す
      for (let j = i - 1; j >= 0; j--) {
        if (tasks.value[j]) {
          tasks.value[i] = tasks.value[j];
          break;
        }
      }
    }
  }
}

// ダミーデータ
const efData = ref([]);


async function submit() {
  // 送信処理を実装

  //いったんtasksをフラットな配列に変換 今後どうするか考える
  
  console.log(tasks.value);
  console.log(`http://127.0.0.1:8000/report/${userID.value}/${day.value}/regi`)

  // tasksをProxy(Array)型からList型（通常の配列）に変換
  const tasksList = Array.isArray(tasks.value) ? [...tasks.value] : [];
  
  const check = {
    start_time: timeSlots.value,
    // end_time: endTime.value,
    successes: successes.value,
    failures: failures.value,
    tasks: tasksList,
  };

  console.log(check);

  const response = await axios.post(
    `http://127.0.0.1:8000/report/${userID.value}/${day.value}/regi`,
    {
      start_time: timeSlots.value,
      successes: successes.value,
      failures: failures.value,
      tasks: tasksList,
    }
  )
  console.log("response", response);
  //efDataの整形
  const ids = [
    ...(response.data.assessment.ef_plus_points || []),
    ...(response.data.assessment.ef_minus_points || [])
  ];
  const uniqueIds = [...new Set(ids)];

  // efDataを生成
  efData.value = uniqueIds.map(id => {
    let score = 0;
    if ((response.data.assessment.ef_plus_points || []).includes(id)) score += 1;
    if ((response.data.assessment.ef_minus_points || []).includes(id)) score -= 1;
    return { EF_item: id, score };
  });
  console.log(response);
  // efData.value = response.data.assessments.items;
  assessment.value = response.data.assessment.assessment;
}


async function re_submit() {
  
  console.log(tasks.value);
  console.log(`http://127.0.0.1:8000/report/${userID.value}/${day.value}/update`)

  // tasksをProxy(Array)型からList型（通常の配列）に変換
  const tasksList = Array.isArray(tasks.value) ? [...tasks.value] : [];
  
  const check = {
    start_time: timeSlots.value,
    // end_time: endTime.value,
    successes: successes.value,
    failures: failures.value,
    tasks: tasksList,
  };

  console.log(check);

  const response = await axios.put(
    `http://127.0.0.1:8000/report/${userID.value}/${day.value}/update`,
    {
      start_time: timeSlots.value,
      successes: successes.value,
      failures: failures.value,
      tasks: tasksList,
    }
  )
  console.log("response", response);
  //efDataの整形
  const ids = [
    ...(response.data.assessment.ef_plus_points || []),
    ...(response.data.assessment.ef_minus_points || [])
  ];
  const uniqueIds = [...new Set(ids)];

  // efDataを生成
  efData.value = uniqueIds.map(id => {
    let score = 0;
    if ((response.data.assessment.ef_plus_points || []).includes(id)) score += 1;
    if ((response.data.assessment.ef_minus_points || []).includes(id)) score -= 1;
    return { EF_item: id, score };
  });
  console.log(response);
  assessment.value = response.data.assessment.assessment;
}


async function save() {
  // 一時保存処理を実装
  try {
    // const response = await axios.post(
    //   'endpoint/{useID}save',
    //   {
    //     startTime: startTime.value,
    //     endTime: endTime.value,
    //     successes: successes.value,
    //     failures: failures.value,
    //     tasks: tasks.value
    //   }
    // )

    // ダミーデータ
    response2 = {
      data: {
        items: [
          { EF_item: "自己管理", score: 1, total_score: 10 },
          { EF_item: "注意力", score: -1, total_score: 8 },
          { EF_item: "感情制御", score: -1, total_score: 9 },
          { EF_item: "計画性", score: 1, total_score: 7 },
          { EF_item: "柔軟性", score: 1, total_score: 12 },
        ],
        assessment:
          "本日の業務は全体的に良好でしたが、注意力に関しては改善の余地があります。特に、タスクの切り替え時に集中力を欠くことがありました。次回は、タスクごとに短い休憩を挟むことで、注意力を高めることをお勧めします。",
      },
    };
  } catch (error) {
    console.error("Error saving data:", error);
  }
}


async function get(inputdate) {

  console.log(`http://127.0.0.1:8000/report/${userID.value}/${inputdate}/get`);
  const response = await axios.post(
    `http://127.0.0.1:8000/report/${userID.value}/${inputdate}/get`,
  )

  console.log(response);
  timeSlots.value = response.data.start_time;
  tasks.value = response.data.tasks 
  successes.value = response.data.successes;
  failures.value = response.data.failures;  

  const ids = [
    ...(response.data.assessment.ef_plus_points || []),
    ...(response.data.assessment.ef_minus_points || [])
  ];
  const uniqueIds = [...new Set(ids)];

  // efDataを生成
  efData.value = uniqueIds.map(id => {
    let score = 0;
    if ((response.data.assessment.ef_plus_points || []).includes(id)) score += 1;
    if ((response.data.assessment.ef_minus_points || []).includes(id)) score -= 1;
    return { EF_item: id, score };
  });

  assessment.value = response.data.assessment.assessment;
}



</script>
