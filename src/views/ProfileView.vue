<template>
  <v-row>
    <v-col cols="4">
      <v-row>
        <v-col cols="6">
          <div class="d-flex align-center justify-end fill-height">
            <p>ニックネーム</p>
          </div>
        </v-col>
        <v-col cols="6">
          <v-text-field
            variant="outlined"
            placeholder="山田たろう"
            type="text"
          ></v-text-field>
        </v-col>
      </v-row>
    </v-col>
    <v-col cols="4">
      <v-row>
        <v-col cols="4">
          <div class="d-flex align-center justify-end fill-height">
            <p>クラス</p>
          </div>
        </v-col>
        <v-col cols="8">
          <v-select :items="classes" label="クラスを選択"></v-select>
        </v-col>
      </v-row>
    </v-col>
    <v-col cols="4">
      <v-row>
        <v-col cols="4">
          <div class="d-flex align-center justify-end fill-height">
            <p>目標設定期間</p>
          </div>
        </v-col>
        <v-col cols="8">
          <v-select
            :items="goal_setting_period"
            label="目標設定期間を選択"
          ></v-select>
        </v-col>
      </v-row>
    </v-col>
  </v-row>

  <v-data-table
    theme="dark"
    :items="items"
    item-value="name"
    v-model="selected"
    show-select
  ></v-data-table>
</template>

<script setup lang="ts">
//DBから取得するクラス一覧をclassesに格納
import { ref } from "vue";

const classes = ["アナリスト", "コンサルタント", "シニアコンサルタント"];
const goal_setting_period = ["3か月間", "6か月間"];

const selected = ref([]);
const items = [
  {
    name: "🍎 Apple",
    location: "Washington",
    height: "0.1",
    base: "0.07",
    volume: "0.0001",
  },
  {
    name: "🍌 Banana",
    location: "Ecuador",
    height: "0.2",
    base: "0.05",
    volume: "0.0002",
  },
  {
    name: "🍇 Grapes",
    location: "Italy",
    height: "0.02",
    base: "0.02",
    volume: "0.00001",
  },
  {
    name: "🍉 Watermelon",
    location: "China",
    height: "0.4",
    base: "0.3",
    volume: "0.03",
  },
  {
    name: "🍍 Pineapple",
    location: "Thailand",
    height: "0.3",
    base: "0.2",
    volume: "0.005",
  },
  {
    name: "🍒 Cherries",
    location: "Turkey",
    height: "0.02",
    base: "0.02",
    volume: "0.00001",
  },
  {
    name: "🥭 Mango",
    location: "India",
    height: "0.15",
    base: "0.1",
    volume: "0.0005",
  },
  {
    name: "🍓 Strawberry",
    location: "USA",
    height: "0.03",
    base: "0.03",
    volume: "0.00002",
  },
  {
    name: "🍑 Peach",
    location: "China",
    height: "0.09",
    base: "0.08",
    volume: "0.0004",
  },
  {
    name: "🥝 Kiwi",
    location: "New Zealand",
    height: "0.05",
    base: "0.05",
    volume: "0.0001",
  },
];
</script>
