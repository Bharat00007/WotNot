<template>

  <!-- New Broadcast Button -->


  <div class="content-section">
    <h2>Broadcast Messages</h2>
    <p>Your content for scheduled broadcasts goes here.</p>
    
    <div class="NeWBroadcastButtonContainer">
      <p>Create a new Broadcast Message</p>
      <button id="NewBroadcastBtn" @click="showPopup = true">New Broadcast</button>
    </div>
    <PopUp v-if="showPopup" @close="showPopup = false">

      <form @submit.prevent="sendMessage" id="messageForm">
        <h3>New Broadcast</h3>
        <label>Broadcast Name</label>
        <input type="text" v-model="broadcastName" placeholder="Broadcast Name" required>

        <label>Recipients</label>
        <input type="text" v-model="recipients" placeholder="Enter phone numbers, comma-separated" required>

        <label for="templates">Choose a template</label>
        <select v-model="selectedTemplate" required>
          <option value="" disabled>Select your option</option>
          <option v-for="template in templates" :key="template.id" :value="template.id">{{ template.name }}</option>
        </select>
        <h3>Contacts</h3>
        <div class="CSVimportContainer">

          <label for="csvFile">Upload CSV:</label>
          <input type="file" @change="handleFileUpload" />
          <button @click.prevent="importCSV">Import</button>
          <a href="https://drive.google.com/file/d/1hVQErwmNN6eGN1zLBoniW_34-GzAtMwm/view?usp=sharing" target="_blank">
            Download Sample CSV</a>
        </div>


        <table class="contact-table">
          <thead>
            <tr>
              <th>Select</th>
              <th>Name</th>
              <th>Phone Number</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="contact in contacts" :key="contact.id">
              <td><input type="checkbox" v-model="selectedContacts" :value="contact.phone"></td>
              <td>{{ contact.name }}</td>
              <td>{{ contact.phone }}</td>
            </tr>
          </tbody>
        </table>


        <button type="submit">Send Message</button>
      </form>
      <div id="response"></div>

    </PopUp>
    <h3>Broadcast list</h3>
    <div class="broadcastListContainer">
      
      <table class="broadcastList-table">
        <thead>
          <tr>
            <th>id</th>
            <th>Broadcast Name</th>
            <th>Template</th>
            <th>Contacts</th>
            <th>Success</th>
            <th>Failed</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>

          <tr v-for="broadcast in broadcasts" :key="broadcast.id">
            <td>{{ broadcast.id }}</td>
            <td>{{ broadcast.name }}</td>
            <td>{{ broadcast.template }}</td>
            <td>{{ broadcast.contacts }}</td>
            <td>{{ broadcast.success }}</td>
            <td>{{ broadcast.failed }}</td>
            <td>{{ broadcast.status }}</td>
          </tr>

        </tbody>
      </table>
    </div>

    <div class="container">
      <!-- Broadcast Form -->

    </div>
  </div>
</template>

<script>

import PopUp from "../popups/popup"
export default {
  name: 'BroadCast2',

  components: {
    PopUp
  }
  ,
  data() {
    return {
      broadcastName: '',
      recipients: '',
      selectedTemplate: '',
      templates: [],
      contacts: [],
      broadcasts: [],
      file: null,
      selectedContacts: [],
      showPopup: false,


    };
  },
  async mounted() {
    await this.fetchTemplates();
    await this.fetchContacts();
    await this.fetchBroadcastList(); 
    
    // Fetch contacts when the component is mounted
  },
  methods: {

  
    async fetchTemplates() {
      try {
        const token = localStorage.getItem('token');
        const response = await fetch('http://localhost:8000/templates/', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        });

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const templateNames = await response.json();
        this.templates = templateNames.map(name => ({ id: name, name }));
      } catch (error) {
        console.error('Error fetching templates:', error);
      }
    },

    async fetchContacts() {

      try {
        const token = localStorage.getItem('token');
        const response = await fetch('http://localhost:8000/contacts/', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        });

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const contactList = await response.json();
        this.contacts = contactList.map(contact => ({
          id: contact.id,
          name: contact.name,
          phone: contact.phone
        }));
      } catch (error) {
        console.error('Error fetching contacts:', error);
      }
    },


    async fetchBroadcastList() {
      const token = localStorage.getItem('token');
      try {
        const response = await fetch('http://localhost:8000/broadcast/', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        });

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const broadcastList = await response.json();
        this.broadcasts = broadcastList.map(broadcast => ({
          id: broadcast.id,
          name: broadcast.name,
          template: broadcast.template,
          contacts: broadcast.contacts,
          success: broadcast.success,
          failed: broadcast.failed,
          status: broadcast.status


        }));
      } catch (error) {
        console.error('Error fetching contacts:', error);
      }
    },

    formatDateTime(date) {
      const day = String(date.getDate()).padStart(2, '0');
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const year = date.getFullYear();
      const hours = String(date.getHours()).padStart(2, '0');
      const minutes = String(date.getMinutes()).padStart(2, '0');
      const seconds = String(date.getSeconds()).padStart(2, '0');

      return `${day}/${month}/${year} ${hours}:${minutes}:${seconds}`;
    },

    updateRecipients() {
      this.recipients = this.selectedContacts.join(', ');
    },

    async sendMessage() {
      const phoneNumbers = this.recipients.split(',').map(num => num.trim());
      const selectedTemplate = this.selectedTemplate;
      const formattedDate = this.formatDateTime(new Date());
      const broadcastNameWithDate = `${this.broadcastName} - ${formattedDate}`;
      const responseDiv = document.getElementById('response');
      responseDiv.textContent = 'Sending...';
      const token = localStorage.getItem('token');

      try {
        const response = await fetch('http://localhost:8000/send-template-message/', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            recipients: phoneNumbers,
            template: selectedTemplate
          }),
        });

        if (!response.ok) {
          throw new Error('Network response was not ok');

        }

        const result = await response.json();
        responseDiv.textContent = `Success: ${result.successful_messages}, Errors: ${result.errors.length}`;

        const logResponse = await fetch('http://localhost:8000/broadcast', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            name: broadcastNameWithDate,
            template: selectedTemplate,
            contacts: phoneNumbers,
            success: result.successful_messages,
            failed: result.errors.length,
            status: result.errors.length > 0 ? 'Partially Successful' : 'Successful'
          }),
        });

        if (!logResponse.ok) {
          throw new Error('Network response was not ok')


        }

        const logResult = await logResponse.json();
        console.log('Broadcast logged:', logResult);
        this.fetchBroadcastList();


      } catch (error) {
        console.error('Error sending messages:', error);
        responseDiv.textContent = 'Error sending messages.';
      }
    },

    handleFileUpload(event) {
      this.file = event.target.files[0];
    },

    async importCSV() {
      if (!this.file) {
        alert('Please select a file to import.');
        return;
      }

      const formData = new FormData();
      formData.append('file', this.file);

      try {
        const response = await fetch('http://localhost:8000/import-contacts', {
          method: 'POST',
          body: formData,
        });

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const data = await response.json();
        this.contacts = data.contacts;
        alert('Contacts imported successfully!');

        // Append phone numbers to the recipients input field
        const phoneNumbers = this.contacts.map(contact => contact.phone).join(',');
        this.recipients = this.recipients ? this.recipients + ',' + phoneNumbers : phoneNumbers;
      } catch (error) {
        console.error(error);
        alert('Failed to import contacts.');
      }
    },

  },
  watch: {
    selectedContacts: function () {
      this.updateRecipients();
    }
  }
};
</script>

<style>
.NeWBroadcastButtonContainer {
  background-color: #f5f6fa;
  border-radius: 12px;
  width: 100%;
  max-width: 1100px;
  padding: 20px;
  display: flex;
  margin-bottom: 20px;
  
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
}

.NeWBroadcastButtonContainer button{
  margin-left: 725px;
 
}

.broadcastListContainer {
  background-color: #f5f6fa;
  border-radius: 12px;
  width: 100%;
  padding: 20px;
  margin-bottom: 20px;
  max-width: 1100px;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);

}

.broadcastList-table {
  width: 100%;
  border-radius: 12px ;
  border-collapse: collapse;
  overflow-x: auto;
  display: block;
  max-height: 400px;
  /* Adjust height as needed */

}

th {
  padding: 20px;
  text-align: left;
  border-collapse: collapse;
  border: 1px solid #ddd;


}

.broadcastList-table td {
  border: 1px solid #ddd;

  padding: 20px;
  text-align: left;
  border-collapse: collapse;
}

.broadcastList-table thead th {
  position: sticky;
  top: 0;
  background-color: #dddddd;
  border-collapse: collapse;
  border: 1px solid #ddd;

}

.broadcastList-table tbody {
  background-color: white;
}

.CSVimportContainer {
  display: flex;
  align-items: center;

}

.CSVimportContainer a {
  padding-left: 10px;
}

.CSVimportContainer input {
  max-width: 200px;
  margin-top: 20px;
  margin-left: 10px;
}

.CSVimportContainer button {
  margin-left: 10px;
  height: 35px;
}


#response {
  margin-top: 20px;
  font-size: 16px;
  color: #333;
}

.contact-table {
  width: auto;

  border-collapse: collapse;
  overflow-x: auto;
  display: block;
  max-height: 200px;
  /* Adjust height as needed */

  margin-bottom: 20px;
}


.contact-table td {
  padding: 15px;
  text-align: left;
  border-collapse: collapse;
  background-color: #ffffff;
}

.contact-table th {
  padding: 15px;
  text-align: left;
  border-collapse: collapse;
}


.contact-table thead th {
  position: sticky;
  top: 0;
  background-color: #dddddd;
  border-collapse: collapse;
}
</style>