// src/router.js
import { createRouter, createWebHashHistory } from 'vue-router';
import BroadCast1 from './components/broadcast/broadcast1.vue';
import BroadCast2 from './components/broadcast/broadcast2.vue';
import BroadCast3 from './components/broadcast/broadcast3.vue';
import ContActs1 from './components/contacts/contacts1.vue';
import ContActs2 from './components/contacts/contacts2.vue';
import MoreOptions1 from './components/more/MoreOptions1.vue';
import LoginPage from './components/login/login.vue';
import DashboardView from './views/dashboardview.vue';

// const routes = [
//   {path: '/login', component: LoginPage, name: 'login'},
//   { path: '/broadcast/broadcast1', component: BroadCast1, name: 'Broadcast1' },
//   { path: '/broadcast/broadcast2', component: BroadCast2, name: 'Broadcast2' },
//   { path: '/broadcast/broadcast3', component: BroadCast3, name: 'Broadcast3' },
//   { path: '/contacts/contacts1', component: ContActs1, name: 'Contacts1' },
//   { path: '/contacts/contacts2', component: ContActs2, name: 'Contacts2' },
//   { path: '/more/more1', component: MoreOptions1, name: 'More1' },
//   { path: '/', redirect: '/broadcast/broadcast2' }
//   // Add other routes here, with `meta: { requiresAuth: true }` for protected routes
  // {path: '/', redirect: '/login/login'} // Default route
// ];

// const router = createRouter({
//   history: createWebHashHistory(), // Use hash mode
//   routes
// });

// Navigation guard to check for authentication
// router.beforeEach((to, from, next) => {
//   const loggedIn = localStorage.getItem('token');
  
//   if (to.matched.some(record => record.meta.requiresAuth) && !loggedIn) {
//     next('/login');
//   } else {
//     next();
//   }
// });

// export default router;


// import { createRouter, createWebHistory } from 'vue-router';
// import Login from '../components/Login.vue';
// import DashboardView from '../views/DashboardView.vue';
// import PublicView from '../views/PublicView.vue';
// import Route1 from '../views/Route1.vue';
// import Route2 from '../views/Route2.vue';
// import Route3 from '../views/Route3.vue';
// import Route4 from '../views/Route4.vue';

const routes = [
  // Public routes
  { path: '/login', component: LoginPage },
  // { path: '/', component: PublicView },

  // Protected routes within the dashboard
  {
    path: '/dashboard',
    component: DashboardView,
     meta: { requiresAuth: true },
    children: [
      { path: '/broadcast/broadcast1', component: BroadCast1, name: 'Broadcast1' },
      { path: '/broadcast/broadcast2', component: BroadCast2, name: 'Broadcast2' },
      { path: '/broadcast/broadcast3', component: BroadCast3, name: 'Broadcast3' },
      { path: '/contacts/contacts1', component: ContActs1, name: 'Contacts1' },
      { path: '/contacts/contacts2', component: ContActs2, name: 'Contacts2' },
      { path: '/more/more1', component: MoreOptions1, name: 'More1' },
      { path: '', redirect: '/broadcast/broadcast2' },
      // Add more routes within the dashboard as needed
    ],
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

// Navigation guard to check for authentication
router.beforeEach((to, from, next) => {
  const loggedIn = localStorage.getItem('token');
  
  if (to.matched.some(record => record.meta.requiresAuth) && !loggedIn) {
    next('/login');
  } else {
    next();
  }
});

export default router;
