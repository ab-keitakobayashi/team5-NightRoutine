<template>
  <v-row>
    <v-col cols="6" class="text-center">
      <vc-calendar expanded :attributes="attributes" />
    </v-col>
    <v-col cols="6" class="text-center">
      <v-card class="pa-5">
        <v-row>
          <v-col cols="6">
            <v-img src="https://picsum.photos/200/300" alt="" class="fluid" />
          </v-col>
          <v-col cols="6">
            <v-card-title class="text-h3 px-5 text-wrap">Lv.1</v-card-title>
            <v-card-text class="text-h5">選択したEF</v-card-text>
            <v-card-text class="text-h5">選択したEF</v-card-text>
            <v-card-text class="text-h5">選択したEF</v-card-text>
            <v-card-text class="text-h5">選択したEF</v-card-text>
            <v-card-text class="text-h5">選択したEF</v-card-text>
            <v-card-text class="text-h5">次のレベルまで</v-card-text>
          </v-col>
        </v-row>
      </v-card>
    </v-col>
  </v-row>
</template>

<script setup lang="ts">
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
</script>
