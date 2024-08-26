<template>
<div class="popup">
    <div class="popup-inner">
        <span class="close" @click="$emit('close')">&times;</span>   
    <slot/>
      
    <!-- <button class="popup-close">Close Popup
    </button> -->
    </div>
</div>
</template>


<script>
export default{
    name:'PopUp'
}
</script>


<style >
.popup{

  position: fixed;
  top: 0;
  right: 0;
  left: 0;
  bottom: 0; 
  background-color:rgba(0, 0, 0, 0.2);
  display: flex;
  justify-content: center;
  
  
  padding: 20px;
  z-index: 10000;
  text-align: left;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);

}
 
.popup-inner{
    background-color:#f5f6fa;
    padding: 20px;
    border-radius: 5px;
    width: 700px;
    overflow-y: auto;
 

}
.close {
    
    padding-left: 680px;
    
    font-size: 24px;
    cursor: pointer;
    color: black;
}
</style>