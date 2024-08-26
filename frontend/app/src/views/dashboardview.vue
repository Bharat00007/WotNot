<template>
  <div id="app">
    <div class="navbar">
     
      <!-- SVG Path here -->
      <div class="nav-left">
        <svg xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 512 512">
        <path fill="#075e54"
          d="M160 368c26.5 0 48 21.5 48 48l0 16 72.5-54.4c8.3-6.2 18.4-9.6 28.8-9.6L448 368c8.8 0 16-7.2 16-16l0-288c0-8.8-7.2-16-16-16L64 48c-8.8 0-16 7.2-16 16l0 288c0 8.8 7.2 16 16 16l96 0zm48 124l-.2 .2-5.1 3.8-17.1 12.8c-4.8 3.6-11.3 4.2-16.8 1.5s-8.8-8.2-8.8-14.3l0-21.3 0-6.4 0-.3 0-4 0-48-48 0-48 0c-35.3 0-64-28.7-64-64L0 64C0 28.7 28.7 0 64 0L448 0c35.3 0 64 28.7 64 64l0 288c0 35.3-28.7 64-64 64l-138.7 0L208 492z" />
      </svg>
        <div class="logo"> WatNot</div>
        <div class="nav-item" v-for="section in navItems" :key="section.name" @click="navigate(section.path)"
          :class="{ active: isActive(section.path) }">
          <i :class="section.icon"></i>{{ section.label }}
        </div>
      </div>

      <!-- logout -->
      <div class="nav-right">
        <div v-if="user">
          
          <p><strong>Email:</strong> {{ user.email }}</p>
          <!-- Display other user details as needed -->
        </div>
        <div v-else>
          <p>Loading user details...</p>
        </div>


        <div class="profile-dropdown" @click="toggleDropdown">
          <img src="../assets/—Pngtree—avatar icon profile icon member_5247852.png" alt="Profile" class="profile-icon" />
          
          <div v-if="dropdownOpen" class="dropdown-menu">
            <ul>
              <li @click="goToProfile"><i class="bi bi-person-circle"></i> View Profile</li>
              <li @click="goToSettings"><i class="bi bi-gear-fill"></i> Settings</li>
              <li @click="logout"><i class="bi bi-box-arrow-right"></i> Logout</li>
            </ul>
          </div>
        </div>
      </div>
      

    </div>

    <div class="content">
      <div class="sidebar" v-if="currentSection === 'broadcast'">
        <a href="#" @click.prevent="navigate('/broadcast/broadcast2')"
          :class="{ active: isActive('/broadcast/broadcast2') }"><i class="bi bi-broadcast"></i>Broadcast Messages</a>
        <a href="#" @click.prevent="navigate('/broadcast/broadcast1')"
          :class="{ active: isActive('/broadcast/broadcast1') }"><i class="bi bi-chat-right-text-fill"></i>Manage
          Templates</a>
        <a href="#" @click.prevent="navigate('/broadcast/broadcast3')"
          :class="{ active: isActive('/broadcast/broadcast3') }"><i class="bi bi-calendar2-range-fill"></i>Scheduled
          Broadcasts</a>
      </div>

      <div class="sidebar" v-if="currentSection === 'Contacts'">
        <a href="#" @click.prevent="navigate('/contacts/contacts1')"
          :class="{ active: isActive('/contacts/contacts1') }"><i class="bi bi-journal-bookmark-fill"></i>Manage
          Contacts</a>
        <a href="#" @click.prevent="navigate('/contacts/contacts2')"
          :class="{ active: isActive('/contacts/contacts2') }"><i class="bi bi-tags-fill"></i>Manage Tags</a>
      </div>

      <div class="sidebar" v-if="currentSection === 'More'">
        <a href="#" @click.prevent="navigate('/more/more1')" :class="{ active: isActive('/more/more1') }">More 1</a>
      </div>

      <div class="main-content">
        <router-view></router-view>
      </div>
    </div>
  </div>
</template>

<script>
import { useRouter, useRoute } from 'vue-router';

export default {
  name: 'DashboardView',
  data() {
    return {
      navItems: [
        { name: 'broadcast', label: 'Broadcast', icon: 'bi bi-broadcast', path: '/broadcast/broadcast2' },
        { name: 'Contacts', label: 'Contacts', icon: 'bi bi-person-video2', path: '/contacts/contacts1' },
        { name: 'More', label: 'More', icon: 'bi bi-three-dots', path: '/more/more1' }
      ],
      user: null,
      dropdownOpen: false,
    }
  },
  setup() {
    const router = useRouter();
    const route = useRoute();
    const isActive = (path) => route.path === path;
    const navigate = (path) => {
      router.push(path);
    }

    return {
      navigate,
      isActive,
      currentSection: getSectionFromRoute(route.path),


    };
  },
  watch: {
    '$route.path': function (newPath) {
      this.currentSection = getSectionFromRoute(newPath);
    }
  },

 
  

 async mounted() {

    await this.created();
    document.addEventListener('click', this.handleOutsideClick);

    // Fetch contacts when the component is mounted
  },
  beforeUnmount() {
    document.removeEventListener('click', this.handleOutsideClick);
  },

  methods: {
    async created() {
      try {
        // Fetch user details on component creation
        const response = await fetch('http://localhost:8000/user', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
          },
        });

        if (!response.ok) {
          throw new Error('Failed to fetch user details');
        }

        this.user = await response.json();
      } catch (error) {
        console.error('Error fetching user details:', error);
        // Optionally handle the error (e.g., show a message to the user)
      }
    },
    
    toggleDropdown() {
      this.dropdownOpen = !this.dropdownOpen;
    },
    goToProfile() {
      // Logic to navigate to profile page
      this.$router.push('/profile');
    },
    goToSettings() {
      // Logic to navigate to settings page
      this.$router.push('/settings');
    },
    logout() {
      // Logic to logout
      localStorage.removeItem('token');
      this.$router.push('/login');
    },

    handleOutsideClick(event) {
      if (!this.$el.contains(event.target)) {
        this.dropdownOpen = false;
      }
    },
  }
}

function getSectionFromRoute(path) {
  if (path.startsWith('/broadcast')) return 'broadcast';
  if (path.startsWith('/contacts')) return 'Contacts';
  if (path.startsWith('/more')) return 'More';
  return 'broadcast';
}
</script>





<style>
body {
  font-family: Arial, sans-serif;
  margin: 0;
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
}

.navbar {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  display: flex;
  justify-content: space-between;
  background-color: #f8f9fa;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  z-index: 1000;
}

.nav-left{
  display: flex;
}

.nav-right{
  display:flex;
  
  align-items: center;
}

.logo {
  font-weight: 800;
  margin: 8px 0 8px 0;
  padding-right: 30px;
  font-size: xx-large;
  color: #075e54;
}

svg {
  width: 32px;
  /* or any desired size */
  height: 32px;
  padding: 15px 10px 10px 10px;
  color: #075e54;
}

.nav-item {
  padding: 15px;
  cursor: pointer;
  color: #333;
  text-align: center;
  margin: 8px 0;
  border-right: 1px solid #e9ecef;
  font-size: medium;
}

.userDetails {
  display: flex;
  margin-left: 300px;
}

.userDetails p {
  padding-left: 5px;
}



.profile-icon {
  width: 60px;
  height: 60px;
  cursor: pointer;
  margin-right:5px;
}

.profile-dropdown {
  position: relative;
  
}

.dropdown-menu {
  position: absolute;
  top: 75px;
  right:30px;
  width: 200px;
  background-color: #ffffff;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  border-radius: 4px;
  overflow: hidden;
}

.dropdown-menu ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.dropdown-menu li {
  padding: 10px;
  cursor: pointer;
  font-size: 18px;
}



.dropdown-menu li:hover {
  background-color: #f1f1f1;
}

.dropdown-menu li i{
  margin-right: 9px;
}

.logout {
  align-self: flex-end;
}

.nav-item i {
  padding-right: 9px;
}

.nav-item:hover {
  font-weight: 600;
  border-radius: 5px;
  color: #075e54;
}

.content {
  display: flex;
  flex: 1;
}

.sidebar {
  position: fixed;
  top: 50px;
  /* Adjust based on navbar height */
  left: 0;
  width: 270px;
  height: calc(100vh - 65px);
  /* Full height minus navbar height */
  background-color: #f5f6fa;
  padding: 10px;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
  overflow-y: auto;
  margin-top: 15px;
  z-index: 999;
  /* Ensure sidebar is above main content */
}

.sidebar a {
  display: block;
  padding: 10px;
  color: #333;
  text-decoration: none;
  margin-bottom: 10px;
  border-radius: 5px;
  font-size: large;
}

.sidebar i {
  padding-right: 10px;
}

.sidebar a:hover {
  font-weight: 600;
  border-radius: 5px;
  color: #075e54;
  background-color: #e9ecef;
}

.sidebar a.active {
  background-color: #075e54;
  color: white;
}

.main-content {
  flex: 1;
  margin-top: 65px;
  margin-left: 300px;
  /* Width of the sidebar */
  padding: 20px;
  height: calc(100vh - 65px);
  /* Full height minus navbar height */
  overflow-y: auto;
  background-color: #ffffff;

  padding: 50px 20px 20px 50px;
  box-sizing: border-box;
  /* Ensure padding does not overflow */
}

.content-section {
  /* Ensure sections have height set if they need to be scrollable */
  height: 100%;

}


.container-contacts {
  background-color: #f5f6fa;
  border-radius: 12px;
  width: 90%;
  max-width: 900px;
  padding: 20px;

  text-align: left;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
}

form {
  display: flex;
  flex-direction: column;
}

select {
  width: 100%;
  padding: 10px;
  margin: 8px 0 20px 0;
  border-radius: 5px;
  border: 1px solid #ccc;
  font-size: 16px;
}

h2 {
  color: #075e54;
  margin-bottom: 20px;
}

input {
  width: calc(100% - 20px);
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #ccc;
  font-size: 16px;
  margin: 8px 0 20px 0;
}

button {
  background-color: #075e54;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 10px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #1ebd5b;
}



</style>