import { createRouter, createWebHistory } from "vue-router";
import LoginView from "../views/LoginView.vue";
import HomeView from "../views/HomeView.vue";
import Calendar from "../views/Calendar.vue";
import EFView from "../views/EFView.vue";
import ProfileView from "../views/ProfileView.vue";
import SummaryView from "../views/Summary.vue";
import CallbackView from "../views/CallbackView.vue";

const routes = [
  { path: "/", component: HomeView, props: false },
  { path: `/reports/show/:inputdate`, component: HomeView, props: true },
  { path: "/login", component: LoginView },
  { path: "/reports/calender", component: Calendar },
  { path: "/reports/EF", component: EFView },
  { path: "/users", component: ProfileView },
  { path: "/summary", component: SummaryView },
  { path: `/callback`, component: CallbackView },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// ★ここからガードを追加
router.beforeEach((to, from, next) => {
  const userId = localStorage.getItem("user_id");
  // ルートパスにアクセスされた場合、今日の日付でリダイレクト
  if (to.path === "/") {
    const today = new Date();
    const yyyy = today.getFullYear();
    const mm = String(today.getMonth() + 1).padStart(2, '0');
    const dd = String(today.getDate()).padStart(2, '0');
    const dateStr = `${yyyy}-${mm}-${dd}`;
    next(`/reports/show/${dateStr}`);
    return;
  }
  // 未ログイン時は /login と /callback 以外にアクセスできない
  if (!userId && to.path !== "/login" && to.path !== "/callback") {
    next("/login");
  } else {
    next();
  }
});
// ★ここまで

export default router;
