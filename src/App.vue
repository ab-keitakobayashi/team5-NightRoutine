<template>
  <v-app>
    <v-app-bar app color="black" dark>
      <v-btn text to="/">振り返り</v-btn>
      <v-btn text to="/reports/calender">カレンダー</v-btn>
      <v-btn text to="/summary">要約</v-btn>
      <v-btn text to="/reports/ef">EF一覧</v-btn>
      <v-btn text to="/users">プロフィール</v-btn>
      <v-spacer></v-spacer>
      <v-toolbar-title
        class="text-center"
        style="justify-content: center; display: flex"
      >
        NightRoutine
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn text to="/login">Login</v-btn>
      <v-btn text @click="logout" v-if="userId">ログアウト</v-btn>
    </v-app-bar>

    <v-main class="full-width bg-grey-darken-4">
      <v-container>
        <router-view />
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";

const email = ref<string | null>(null);
const userId = ref<string | null>(null);
const router = useRouter();

// ログアウト処理
function logout() {
  localStorage.removeItem("user_email");
  localStorage.removeItem("user_id");
  email.value = null;
  userId.value = null;
  router.push("/login");
}

onMounted(() => {
  email.value = localStorage.getItem("user_email");
  userId.value = localStorage.getItem("user_id");

  // ストレージ変更イベントにも対応（他タブや動的変更時）
  window.addEventListener("storage", () => {
    email.value = localStorage.getItem("user_email");
    userId.value = localStorage.getItem("user_id");
    if (!userId.value) {
      router.push("/login");
    }
  });
});
</script>
<style scoped>
.full-width {
  padding-right: 0;
  padding-left: 0;
  margin-right: 0;
  margin-left: 0;
}
</style>
