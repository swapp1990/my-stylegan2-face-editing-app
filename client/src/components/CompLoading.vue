<template>
  <div>
    <button type="button" class="loading" v-b-tooltip.hover :title="getTitle">
      <i v-if="isLoadingFlag == 1" class="fas fa-spinner fa-spin icon fa-fw"></i>
      <i v-if="isLoadingFlag == 0" class="fas fa-check fa-fw"></i>
      <i v-if="isLoadingFlag == 2" class="fas fa-exclamation-triangle red"></i>
    </button>
  </div>
</template>

<script>
export default {
  name: "compLoading",
  props: ["isLoadingFlag"], //0: loaded, 1: loading, 2: error
  watch: {
    isLoadingFlag() {},
    deep: true,
    immediate: true,
  },
  methods: {
    getTitle() {
      if (this.isLoadingFlag == 2) {
        return "Server is down";
      }
      return this.isLoadingFlag == 1 ? "Loading" : "Loaded";
    },
  },
};
</script>

<style lang="scss" scoped>
$color-red: #d30320;
$color-black: rgb(0, 0, 0);
%overlayBtn {
  background: transparent;
  outline: none;
  border: none;
  cursor: pointer;
  &:hover {
    color: darken(rgba($color-black, 0.95), 8%);
    opacity: 1;
  }
}
.loading {
  @extend %overlayBtn;
  i.red {
    color: darken(rgba($color-red, 0.95), 8%);
  }
}
</style>