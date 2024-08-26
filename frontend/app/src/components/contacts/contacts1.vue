<template>
    <div class="content-section">
        <button @click="showPopup = true">Add Contact</button>
        <PopUp v-if="showPopup" @close="showPopup = false">
            <form @submit.prevent="submitForm" id="contactForm">
                <input type="hidden" v-model="contact.id" id="contactId">
                <input type="text" v-model="contact.name" id="name" placeholder="Name" required>
                <input type="email" v-model="contact.email" id="email" placeholder="Email" required>
                <input type="text" v-model="contact.phone" id="phone" placeholder="Phone" required>
                <input type="text" v-model="contact.tags" id="tags" placeholder="Tags (comma separated)">
                <button type="submit">Add Contact</button>
            </form>
        </PopUp>
        <div class="container-contacts">
            <h3>Contact Directory</h3>

            <!-- Search and Display Contacts -->
            <div class="search">
                <input type="text" v-model="searchPhone" id="searchPhone" placeholder="Search by Phone">
                <button @click="searchContact">Search</button>
            </div>

            <div id="contactsList">
                <div v-for="contact in contacts" :key="contact.id">
                    <p>{{ contact.name }} - {{ contact.phone }}</p>
                </div>
            </div>
        </div>
    </div>
</template>


<script>
import PopUp from "../popups/popup"
export default {

    components:{
        PopUp
    },

    name:'ContActs1',
  data() {
    return {
      showPopup: false,
      contact: {
        id: '',
        name: '',
        email: '',
        phone: '',
        tags: ''
      },
      searchPhone: '',
      contacts: []
    };
  },
  methods: {
    async submitForm() {
      const { id, name, email, phone, tags } = this.contact;
      const tagArray = tags.split(',').map(tag => tag.trim());
      const url = id ? `http://localhost:8000/contacts/phone/${phone}` : 'http://localhost:8000/contacts/';
      const method = id ? 'PUT' : 'POST';
      const token = localStorage.getItem('token'); 
      
      try {
        const response = await fetch(url, {
          method: method,
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ name, email, phone, tags: tagArray }),
        });

        if (response.ok) {
          alert('Contact saved successfully');
          this.clearForm();
          this.loadContacts();
        } else {
          const errorData = await response.json();
          alert(`Error: ${errorData.detail}`);
        }
      } catch (error) {
        console.error('Error saving contact:', error);
        alert('Error saving contact');
      }
    },
    clearForm() {
      this.contact = {
        id: '',
        name: '',
        email: '',
        phone: '',
        tags: ''
      };
      this.showPopup = false;
    },
    async loadContacts() {
      try {
        const response = await fetch('http://localhost:8000/contacts/');
        this.contacts = await response.json();
      } catch (error) {
        console.error('Error loading contacts:', error);
      }
    },
    async searchContact() {
      try {
        const response = await fetch(`http://localhost:8000/contacts/phone/${this.searchPhone}`);
        if (response.ok) {
          const contact = await response.json();
          this.contacts = [contact];
        } else {
          alert('Contact not found');
        }
      } catch (error) {
        console.error('Error searching contact:', error);
        alert('Error searching contact');
      }
    }
  },
  mounted() {
    this.loadContacts();
  }
};
</script>


<style scoped>
/* Add your styles here */
</style>