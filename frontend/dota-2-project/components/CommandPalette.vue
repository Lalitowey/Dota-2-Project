<script setup lang="ts">
  import { ref, wathc } from 'vue';
  import { vueRouter } from 'vue-router';
  import { CommandDialog, CommandEmpty, CommandGroup, CommandInput, CommandItem, CommandList } from '@/components/ui/command';
  import { useDebounceFn } from '@vueuse/core'; // For debouncing AI calls.

  const props = defineProps<{ open: boolean }>();
  const emit = defineEmits(['update:open']);
  const router = useRouter();
  
</script>

<template>
</template>

<style scoped>

</style>
