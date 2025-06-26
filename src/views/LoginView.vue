<template>
  <v-img src="/assets/bg.png" class="d-flex align-center justify-center">
    <v-row
      align="center"
      justify="center"
      class="ma-0 pa-0"
      style="width: 100%; position: absolute; bottom: 32px; left: 0"
    >
      <v-col cols="3" class="d-flex justify-center mt-5 pt-5">
        <v-btn @click="login" color="grey-lighten-5" block class="pa-7"
          >ログイン</v-btn
        >
      </v-col>
    </v-row>
  </v-img>
</template>

<script setup lang="ts">
// コグニートに飛ぶロジックを追加
async function login() {
  console.log("ログインボタンがクリックされました");
}
</script>

<style scoped></style>
