<template>
  <v-table theme="dark">
    <thead>
      <tr>
        <th>クラス</th>
        <th>Sub Dimension</th>
        <th>Detailed Category</th>
        <th>EF項目</th>
        <th>合計点</th>
        <th>得点月日</th>
      </tr>
    </thead>
    <tbody>
      <tr
        v-for="(item, idx) in efData"
        :key="idx"
        :class="idx < 5 ? 'bg-grey-darken-3' : ''"
      >
        <td>{{ item.class }}</td>
        <td>{{ item.sub_dimension }}</td>
        <td>{{ item.detailed_category }}</td>
        <td>{{ item.item }}</td>
        <td>{{ item.total_score }}</td>
        <td>
          <ul>
            <li v-for="(d, i) in item.score_dates" :key="i">
              <v-btn
                color="indigo-darken-4"
                size="small"
                @click="onDateClick(d)"
              >
                {{ d.date }}
              </v-btn>
            </li>
          </ul>
        </td>
      </tr>
    </tbody>
  </v-table>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";

const items = ref([]);
const efData = ref([]);

async function onDateClick(d) {
  // ここにクリック時の処理を書く（例：アラート表示）
  alert(`日付: ${d.date}`);
}
async function show() {
  // const response = await axios.post(
  //   'endpoint/reports/EF/{useID}',
  //   {
  //     startTime: startTime.value,
  //     endTime: endTime.value
  //   }
  // )

  // ダミーデータ
  const items = [
    {
      sub_dimension: "自己統制",
      detailed_category: "自己管理",
      class: "Consultant",
      item: "上位者の指示に従ってタスクの時間管理ができる",
      total_score: 10,
      score_dates: [
        { date: "2025-06-01" },
        { date: "2025-06-15" },
        { date: "2025-06-25" },
      ],
    },
    {
      sub_dimension: "注意力制御",
      detailed_category: "注意力",
      class: "Consultant",
      item: "集中力を維持し、タスクに集中できる",
      total_score: 8,
      score_dates: [
        { date: "2025-06-01" },
        { date: "2025-06-15" },
        { date: "2025-06-25" },
      ],
    },
    {
      sub_dimension: "感情制御",
      detailed_category: "感情制御",
      class: "Consultant",
      item: "ストレス管理ができ、感情を適切に制御できる",
      total_score: 9,
      score_dates: [{ date: "2025-06-10" }, { date: "2025-06-24" }],
    },
    {
      sub_dimension: "計画性",
      detailed_category: "計画性",
      class: "Senior Consultant",
      item: "タスクを計画的に進め、期限内に完了できる",
      total_score: 7,
      score_dates: [{ date: "2025-06-03" }, { date: "2025-06-18" }],
    },
    {
      sub_dimension: "柔軟性",
      detailed_category: "柔軟性",
      class: "Consultant",
      item: "変化に柔軟に対応し、適応力がある",
      total_score: 12,
      score_dates: [{ date: "2025-06-08" }, { date: "2025-06-22" }],
    },
    {
      sub_dimension: "柔軟性",
      detailed_category: "柔軟性",
      class: "Consultant",
      item: "変化に柔軟に対応し、適応力がある",
      total_score: 12,
      score_dates: [{ date: "2025-06-08" }, { date: "2025-06-22" }],
    },
    {
      sub_dimension: "柔軟性",
      detailed_category: "柔軟性",
      class: "Consultant",
      item: "柔軟に対応し、適応力があり、変化に対応できる",
      total_score: -12,
      score_dates: [{ date: "2025-06-08" }, { date: "2025-06-22" }],
    },
    {
      sub_dimension: "柔軟性",
      detailed_category: "柔軟性",
      class: "Consultant",
      item: "変化に柔軟に対応し、適応力があり、変化に対応でき、柔軟性がある",
      total_score: -2,
      score_dates: [{ date: "2025-06-08" }, { date: "2025-06-22" }],
    },
    {
      sub_dimension: "柔軟性",
      detailed_category: "柔軟性",
      class: "Consultant",
      item: "変化に柔軟に対応し、適応力があるだけでなく、柔軟性も高い",
      total_score: -1,
      score_dates: [{ date: "2025-06-08" }, { date: "2025-06-22" }],
    },
  ];

  efData.value = items;
}

// ページ表示時にshow()を呼び出す
onMounted(() => {
  show();
});
</script>

<style>
li {
  list-style: none;
}
</style>
