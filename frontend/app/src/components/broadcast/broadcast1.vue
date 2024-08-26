<template>
  <div class="content-section">

    <h2>Manage Templates</h2>
    <p>Your content for scheduled broadcasts goes here.</p>

    <div class="CreateTemplateContainer">
      <p>Create New Template</p>
      <button @click="showSelectionPopup = true">Create Template</button>
    </div>

    <div class="templateList_container">
      <table class="templateList-table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Language</th>
            <th>Status</th>
            <th>Category</th>
            <th>Sub Category</th>
            <th>ID</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="template in templates" :key="template.id">
            <td>{{ template.name }}</td>
            <td>{{ template.language }}</td>
            <td>{{ template.status }}</td>
            <td>{{ template.category }}</td>
            <td>{{ template.sub_category }}</td>
            <td>{{ template.id }}</td>
            <td><button id="TemplatedeleteBtn">Delete</button></td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Popup for Template Type Selection -->
    <div v-if="showSelectionPopup" class="popup-overlay" @click.self="closeSelectionPopup">
      <div class="popup-content">
        <h2>Select Template Type</h2>
        <div class="template-type-options">
          <button @click="selectType('MARKETING')">Marketing</button>
          <button @click="selectType('UTILITY')">Utility</button>
        </div>
        <button @click="closeSelectionPopup" class="discard-button">Close</button>
      </div>
    </div>

    <!-- Create Template Popup -->
    <div v-if="showPopup" class="popup-overlay" @click.self="closePopup">
      <div class="popup-content">
        <h2>Create {{ selectedType }} Template</h2>
        <form @submit.prevent="submitTemplate">
          <input v-model="template.name" placeholder="Template Name" required />
          <textarea v-model="bodyComponent.text" placeholder="Body Text" required></textarea>

          <!-- Conditionally display header component -->
          <input v-model="headerComponent.text" placeholder="Header Text (optional)" />

          <!-- Conditionally display footer component -->
          <input v-model="footerComponent.text" placeholder="Footer Text (optional)" />

          <!-- Conditionally display button component -->
          <input v-if="selectedSubCategory !== 'ORDER_STATUS'" v-model="button.text" placeholder="Button Text (optional)" />
          <input v-if="selectedSubCategory !== 'ORDER_STATUS'" v-model="button.url" placeholder="Button URL (optional)" />

          <!-- New Dropdown for Sub-Category Selection -->
          <select v-model="selectedSubCategory" required>
            <option value="" disabled>Select Sub-Category</option>
            <option value="ORDER_DETAILS">Order Details</option>
            <option value="ORDER_STATUS">Order Status</option>
          </select>

          <button type="submit" class="submit-button">Submit</button>
        </form>
        <button @click="closePopup" class="discard-button">Close</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'BroadCast1',
  data() {
    return {
      templates: [],
      showPopup: false,
      showSelectionPopup: false,
      selectedType: '',
      selectedSubCategory: '',
      template: {
        name: '',
        components: []
      },
      bodyComponent: {
        type: 'BODY',
        text: ''
      },
      headerComponent: {
        type: 'HEADER',
        format: 'TEXT',
        text: ''
      },
      footerComponent: {
        type: 'FOOTER',
        text: ''
      },
      button: {
        type: 'URL',
        text: '',
        url: ''
      }
    };
  },

  async mounted() {
    await this.fetchtemplateList();
  },

  methods: {
    async fetchtemplateList() {
      const token = localStorage.getItem('token');
      try {
        const response = await fetch("http://localhost:8000/template", {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          }
        });

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const templatelist = await response.json();
        this.templates = templatelist.data;
      } catch (error) {
        console.error("There was an error fetching the templates:", error);
      }
    },

    selectType(type) {
      this.selectedType = type;
      this.showSelectionPopup = false;
      this.showPopup = true;
    },

    async submitTemplate() {
      this.template.components = [this.bodyComponent];

      if (this.selectedSubCategory !== 'ORDER_STATUS') {
        if (this.headerComponent.text) {
          this.template.components.push(this.headerComponent);
        }

        if (this.footerComponent.text) {
          this.template.components.push(this.footerComponent);
        }

        if (this.button.text && this.button.url) {
          this.template.components.push({
            type: 'BUTTONS',
            buttons: [this.button]
          });
        }
      } else {
        if (this.footerComponent.text) {
          this.template.components.push(this.footerComponent);
        }
      }

      const payload = {
        name: this.template.name,
        components: this.template.components,
        language: 'en_US',
        category: this.selectedType,
        sub_category: this.selectedSubCategory
      };

      const token = localStorage.getItem('token');

      if (!token) {
        console.error('No access token found in local storage');
        return;
      }

      try {
        const response = await axios.post('http://localhost:8000/create-template', payload, {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });

        console.log('Template created successfully:', response.data);

        await this.fetchtemplateList();
        this.closePopup();
      } catch (error) {
        console.error('Error creating template:', error.response ? error.response.data : error.message);
      }
    },

    closeSelectionPopup() {
      this.showSelectionPopup = false;
      this.selectedType = '';
    },
    closePopup() {
      this.showPopup = false;
      this.template.name = '';
      this.bodyComponent.text = '';
      this.headerComponent.text = '';
      this.footerComponent.text = '';
      this.button.text = '';
      this.button.url = '';
      this.selectedSubCategory = '';
    }
  }
}
</script>

<style scoped>
/* General styles */
table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  border: 1px solid #ddd;
  padding: 8px;
}

th {
  background-color: #f2f2f2;
}

.CreateTemplateContainer {
  background-color: #f5f6fa;
  border-radius: 12px;
  width: 100%;
  max-width: 1100px;
  padding: 20px;
  display: flex;
  margin-bottom: 20px;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
}

.CreateTemplateContainer button {
  margin-left: 805px;
}

.templateList_container {
  background-color: #f5f6fa;
  border-radius: 12px 12px;
  width: 100%;
  padding: 20px;
  margin-bottom: 20px;
  max-width: 1100px;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
}

.templateList-table {
  width: 100%;
  border-radius: 12px 12px;
  border-collapse: collapse;
  overflow-x: auto;
  display: block;
  max-height: 400px;
}

th {
  padding: 20px 43px;
  text-align: left;
  border-collapse: collapse;
  border: 1px solid #ddd;
}

.templateList-table td {
  border: 1px solid #ddd;
  padding: 20px;
  text-align: left;
  border-collapse: collapse;
}

.templateList-table thead th {
  position: sticky;
  top: 0;
  background-color: #dddddd;
  border-collapse: collapse;
  border: 1px solid #ddd;
}

.templateList-table tbody {
  background-color: white;
}

/* Popup Styles */
.popup-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.popup-content {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  max-width: 400px;
  width: 100%;
}

.template-type-options {
  display: flex;
  justify-content: space-between;
  gap: 20px;
}

.template-type-options button {
  flex: 1;
  padding: 10px;
  border: none;
  background-color: #218838;
  color: white;
  border-radius: 5px;
  cursor: pointer;
}

.template-type-options button:hover {
  background-color: #218838;
}

.discard-button {
  margin-top: 20px;
  background-color: #ff4d4d;
  color: white;
  border: none;
  padding: 10px;
  border-radius: 5px;
  cursor: pointer;
}

.submit-button {
  background-color: #28a745;
  color: white;
  border: none;
  padding: 10px;
  border-radius: 5px;
  cursor: pointer;
}

.submit-button:hover {
  background-color: #218838;
}

</style>
