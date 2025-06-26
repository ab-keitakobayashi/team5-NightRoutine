<template>
  <v-alert
    v-if="errorMessage"
    type="error"
    color="red"
    variant="elevated"
    class="mb-4"
  >
    {{ errorMessage }}
  </v-alert>
  <v-row>
    <v-col cols="3">
      <v-row>
        <v-col cols="4">
          <div class="d-flex align-center justify-end fill-height">
            <p>ニックネーム</p>
          </div>
        </v-col>
        <v-col cols="8">
          <v-text-field
            v-model="user_name"
            variant="outlined"
            placeholder="山田たろう"
            type="text"
          ></v-text-field>
        </v-col>
      </v-row>
    </v-col>
    <v-col cols="3">
      <v-row>
        <v-col cols="3">
          <div class="d-flex align-center justify-end fill-height">
            <p>クラス</p>
          </div>
        </v-col>
        <v-col cols="9">
          <v-select
            v-model="user_class_id"
            :items="classes"
            label="クラスを選択"
          ></v-select>
        </v-col>
      </v-row>
    </v-col>
    <v-col cols="4">
      <v-row>
        <v-col cols="5">
          <div class="d-flex align-center justify-end fill-height">
            <p>目標設定期間</p>
          </div>
        </v-col>
        <v-col cols="7">
          <v-select
            v-model="user_goal_setting_period"
            :items="goal_setting_period"
            label="目標設定期間選択"
          ></v-select>
        </v-col>
      </v-row>
    </v-col>
    <v-col cols="2">
      <v-btn @click="save_profile" x-large color="warning" variant="outlined"
        >保存</v-btn
      >
    </v-col>
  </v-row>

  <v-data-table
    theme="dark"
    :headers="headers"
    :items="items"
    item-value="value"
    v-model="ef_item_ids"
    show-select
    ><template v-slot:header.EF_class="{ column }"
      ><span>{{ column.text }}</span></template
    >
    <template v-slot:header.parent_category_id="{ column }"
      ><span>{{ column.text }}</span></template
    >
    <template v-slot:header.child_category_id="{ column }"
      ><span>{{ column.text }}</span></template
    >
    <template v-slot:header.item="{ column }"
      ><span>{{ column.text }}</span></template
    >
  </v-data-table>
</template>

<script setup lang="ts">
const classes = [
  { title: "アナリスト", value: 1 },
  { title: "コンサルタント", value: 2 },
  { title: "シニアコンサルタント", value: 3 },
];

const goal_setting_period = [
  { title: "3ヶ月", value: 3 },
  { title: "6ヶ月", value: 6 },
  { title: "1年", value: 12 },
];

const headers = [
  { text: "クラス", value: "EF_class" },
  { text: "親カテゴリー", value: "parent_category_id" },
  { text: "子カテゴリー", value: "child_category_id" },
  { text: "EF項目", value: "item" },
];

// EF項目のデータをDBから取得する
// ここではダミーデータを使用
const items = [
  {
    EF_class: "アナリスト",
    parent_category_id: "知識",
    child_category_id: "ロジカルシンキング",
    item: "上位者の指示に従って行動する",
    value: 1,
  },
  {
    EF_class: "アナリスト",
    parent_category_id: "知識",
    child_category_id: "ロジカルシンキング",
    item: "自分の意見を持ち、発言する",
    value: 2,
  },
  {
    EF_class: "アナリスト",
    parent_category_id: "知識",
    child_category_id: "ロジカルシンキング",
    item: "チームの目標を理解し、貢献する",
    value: 3,
  },
  {
    EF_class: "アナリスト",
    parent_category_id: "チームワーク",
    child_category_id: "責任感",
    item: "問題解決のために積極的に行動する",
    value: 4,
  },
  {
    EF_class: "アナリスト",
    parent_category_id: "チームワーク",
    child_category_id: "責任感",
    item: "新しいアイデアを提案する",
    value: 5,
  },
  {
    EF_class: "アナリスト",
    parent_category_id: "チームワーク",
    child_category_id: "行動力",
    item: "他のメンバーと協力して作業する",
    value: 6,
  },
  {
    EF_class: "アナリスト",
    parent_category_id: "技術",
    child_category_id: "柔軟性",
    item: "フィードバックを受け入れ、改善する",
    value: 7,
  },
  {
    EF_class: "アナリスト",
    parent_category_id: "技術",
    child_category_id: "柔軟性",
    item: "自分の感情を適切に管理する",
    value: 8,
  },
  {
    EF_class: "アナリスト",
    parent_category_id: "技術",
    child_category_id: "タスク管理",
    item: "タスクを効率的に管理する",
    value: 9,
  },
  {
    EF_class: "アナリスト",
    parent_category_id: "技術",
    child_category_id: "タスク管理",
    item: "変化に柔軟に対応する",
    value: 10,
  },
];
import { ref } from "vue";
import axios from "axios";

const user_name = ref("");
// アナリスト＝1, コンサルタント＝2, シニアコンサルタント＝3
const user_class_id = ref();
// 目標設定期間は3ヶ月＝3、6ヶ月=6、1年=12
const user_goal_setting_period = ref();
// 選択されたEFのIDを格納する
const ef_item_ids = ref([]);

const errorMessage = ref("");

async function save_profile() {
  errorMessage.value = "";

  if (!user_name.value) {
    errorMessage.value = "ニックネームを入力してください。";
    return;
  }
  if (!user_class_id.value) {
    errorMessage.value = "クラスを選択してください。";
    return;
  }
  if (!user_goal_setting_period.value) {
    errorMessage.value = "期間を選択してください。";
    return;
  }
  if (ef_item_ids.value.length !== 5) {
    errorMessage.value = "EF項目は5つ選択してください。";
    return;
  }
  // ここにプロフィール保存のロジックを追加
  console.log(
    user_name.value,
    user_class_id.value,
    user_goal_setting_period.value,
    ef_item_ids.value
  );


  const ef_item_id_array = Array.isArray(ef_item_ids.value) ? [...ef_item_ids.value] : [];
  const response = await axios.post(
    `http://127.0.0.1:8000/user/regi`,
    {
      name: user_name.value,
      class_id: user_class_id.value,
      period: user_goal_setting_period.value,
      ef_item_id_array: ef_item_id_array,
    }
  )
  console.log(response);
  if (response.status === 200) {
    alert("プロフィールが保存されました。");
  } else {
    errorMessage.value = "プロフィールの保存に失敗しました。";
  }
}
</script>
