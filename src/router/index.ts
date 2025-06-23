import { createRouter, createWebHistory } from "vue-router";
import LoginView from "../views/LoginView.vue";
import HomeView from "../views/HomeView.vue";
import Calendar from "../views/Calendar.vue";
import EFView from "../views/EFView.vue";
import ProfileView from "../views/ProfileView.vue";

const routes = [
  { path: "/", component: HomeView },
  { path: "/login", component: LoginView },
  { path: "/reports/calender", component: Calendar },
  { path: "/reports/EF", component: EFView },
  { path: "/users", component: ProfileView },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
