<template>
  <v-row>
    <v-col cols="6" class="text-center">
      <vc-calendar expanded :attributes="attributes" />
    </v-col>
    <v-col cols="6" class="text-center">
      <v-row>
        <v-col cols="12">
          <v-card>
            <v-card-item>
              <v-card-title>Lv.</v-card-title>

              <v-card-subtitle>This is a card subtitle</v-card-subtitle>
            </v-card-item>

            <v-card-text>
              Lorem ipsum dolor sit amet consectetur adipisicing elit. Commodi,
              ratione debitis quis est labore voluptatibus!
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-col>
  </v-row>
</template>

<script setup lang="ts">
const attributes = [
  {
    key: "holidays",
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
    key: "events",
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
