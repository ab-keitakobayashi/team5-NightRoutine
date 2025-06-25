<template>
  <v-row>
    <v-col cols="6">
      <v-row>
        <v-col cols="4">
          <p>開始日時</p>
          <v-text-field
            variant="outlined"
            v-model="startDateTimeDisplay"
            placeholder="例: 2025-06-25"
            readonly
            @click="dateDialog = true"
          ></v-text-field>

          <v-dialog v-model="dateDialog" persistent width="290">
            <v-card>
              <v-date-picker v-model="date" :max="maxDate"></v-date-picker>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="primary" text @click="setDateTime">決定</v-btn>
                <v-btn text @click="dateDialog = false">キャンセル</v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-col>
        <v-col cols="4">
          <p>終了日時</p>
          <v-text-field
            variant="outlined"
            v-model="endDateTimeDisplay"
            placeholder="例: 2025-06-25"
            readonly
            @click="endDateDialog = true"
          ></v-text-field>

          <v-dialog v-model="endDateDialog" persistent width="290">
            <v-card>
              <v-date-picker v-model="endDate" :max="maxDate"></v-date-picker>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="primary" text @click="setEndDateTime">決定</v-btn>
                <v-btn text @click="endDateDialog = false">キャンセル</v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-col>
        <v-col cols="4">
          <v-btn @click="summary" class="text-black ma-5"> 要約 </v-btn>
        </v-col>
      </v-row>
      <p>AI評価</p>
      <v-table theme="dark">
        <thead>
          <tr>
            <th>EF項目</th>
            <th>合計ポイント</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, idx) in efData" :key="idx">
            <td>{{ item.EF_item }}</td>
            <td>{{ item.total_score }}</td>
          </tr>
        
        </tbody>
      </v-table>
    </v-col>
    <v-col cols="6">
      <p>AIコメント</p>
      <v-textarea
        v-model="assessment"
        bg-color="grey-darken-3"
        variant="outlined"
        name="assessment"
        placeholder="AIが要約を出力します"
        rows="18"
        auto-grow
        outlined
      ></v-textarea>
    </v-col>
  </v-row>
</template>

<script setup>
import { ref, computed } from "vue";

// 開始日時用
const dateDialog = ref(false)
const date = ref('Tue Jun 25 2025 00:00:00') // 初期値を設定

const startDate = ref("");
const startDateTimeDisplay = computed({
  get() {
     console.log("startDateTimeDisplay called")
     console.log("date:", date.value)
    if (date.value ) {
      console.log("startDateTimeDisplay:", date.value)
      return `${formatDate(date.value)}`
    }
    return ''
  },
  set(val) {
    // 外部からの直接セットは不要
  }
})

function setDateTime() {
    console.log("setDateTime called")
    console.log("date:", date.value)
  if (date.value) {
    startDate.value = `${date.value}`
    dateDialog.value = false
    console.log(dateDialog.value)
  }
}

// 終了日時用
const endDateDialog = ref(false)
const endDate = ref('Tue Jun 25 2025 00:00:00')

const endDateTimeDisplay = computed({
  get() {
    if (endDate.value) {
     return `${formatDate(endDate.value)}`
    }
    return ''
  },
  set(val) {
    // 外部からの直接セットは不要
  }
})

function setEndDateTime() {
  if (endDate.value) {
    endDate.value = `${endDate.value} `
    endDateDialog.value = false
  }
}

// その他
const successes = ref('');
const failures = ref('');
const assessment = ref('');
const item = ref({});
const tasks = ref([]);

// 最大日付（今日まで選択可能）
const maxDate = new Date().toISOString().substr(0, 10)


// yyyy-mm-dd表示用
function pad(num) {
  return num.toString().padStart(2, '0')
}

function formatDate(dateObj) {
  if (!dateObj) return ''
  const d = new Date(dateObj)
  const yyyy = d.getFullYear()
  const mm = pad(d.getMonth() + 1)
  const dd = pad(d.getDate())
  return `${yyyy}-${mm}-${dd}`
}

function formatTime(timeObj) {
  if (!timeObj) return ''
  // timeObjが"HH:mm"形式ならそのまま返す
  if (typeof timeObj === 'string') return timeObj
  // Date型の場合
  const d = new Date(timeObj)
  return `${pad(d.getHours())}:${pad(d.getMinutes())}`
}
// yyyy-mm-dd表示用ここまで



// ダミーデータ
const efData = ref([
  { EF_item: "自己管理",  total_score: 0 },
  { EF_item: "注意力", total_score: 0 },
  { EF_item: "感情制御",  total_score: 0 },
  { EF_item: "計画性",  total_score: 0 },
  { EF_item: "柔軟性", total_score: 0 },
]);



async function summary() {
  // 送信処理を実装

    //responseにAPIからのデータが返ってくる
   const check = {
        startDate: startDate.value,
        endDate: endDate.value,
      }

    console.log(check);
    
    // const response = await axios.post(
    //   'endpoint/summary/{useID}',
    //   {        
    //     startTime: startTime.value,
    //     endTime: endTime.value
    //   }
    // )

    // ダミーデータ
    const response = {
       data: {
            items: [
              { EF_item: "自己管理",  total_score: 10 },
              { EF_item: "注意力",  total_score: 8 },
              { EF_item: "感情制御", total_score: 9 },
              { EF_item: "計画性",  total_score: 7 },
              { EF_item: "柔軟性",  total_score: 12 }
            ],
            summary: "要約結果が返ってきました"
      }
      }

    efData.value = response.data.items;
    assessment.value = response.data.summary;

}

</script>
<style>
html, body, #app {
  margin: 0;
  padding: 0;
  width: 100vw;
  min-height: 100vh;
  background: #000;
  box-sizing: border-box;
  overflow-x: hidden;
}
</style>