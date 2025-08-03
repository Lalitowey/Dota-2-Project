<script setup lang="ts">
import { ref, watch } from 'vue';
import { useMagicKeys } from '@vueuse/core';
import AppSidebar from '@/components/sidebar.vue';
import AppNavbar from '@/components/AppNavbar.vue';
import CommandPalette from '@/components/CommandPalette.vue'

const open = ref(false);
const keys = useMagicKeys();
const CtrlK = keys['Ctrl + K'];
const CmdK = keys['Cmd + K'];

watch([CtrlK, CmdK], (v) => {
  if(v) {
    open.value = !open.value;
  }
});
</script>

<template>
  <div class="flex h-screen bg-background">
    <sidebar/>
    <div class="flex-1 flex flex-col overflow-hidden">

      <AppNavbar/>
      <main class="flex-1 p-4 md:p-6 lg:p-8 overflow-y-auto">
        <slot/>
      </main>
    </div>
  </div>
</template>
