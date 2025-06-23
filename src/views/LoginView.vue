<template>
  <v-row align="center" justify="center">
    <v-col cols="12">
      <v-card>
        <v-card-title class="text-h5">ログイン</v-card-title>
        <v-card-text>
          <v-form>
            <v-text-field label="メールアドレス" required></v-text-field>
            <v-text-field
              label="パスワード"
              type="password"
              required
            ></v-text-field>
            <v-btn color="primary" block>ログイン</v-btn>
          </v-form>
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</template>

<script setup lang="ts">
// 必要に応じてロジックを追加
</script>
