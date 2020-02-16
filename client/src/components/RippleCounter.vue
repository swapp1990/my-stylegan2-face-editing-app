<template>
    <div class="ripple-counter" v-bind:class="{ animate: triggerAnimation }">
        <span>{{txt}}</span>
    </div>
</template>

<script>
    export default {
        name: "rippleCounter",
        props: ["txt"],
        watch: { 
            txt: { // watch it
            immediate: true, 
                handler(val, oldVal) {
                    // console.log('Prop changed: ', val, ' | was: ', oldVal);
                    this.triggerAnimation = true;
                    setTimeout(() => {
                        this.triggerAnimation = false;
                    }, 1000);
                }
            }
        },
        data() {
            return {
                triggerAnimation: false,
                txtData: "test"
            }
        }
    }
</script>

<style lang="scss" scoped>
.animate {
    &::after {
        animation-name: ripple;
        animation-duration: 1s;
        animation-delay: 0s;
        animation-iteration-count: 1;
        animation-timing-function: cubic-bezier(.65,0,.34,1);
    }
}

@mixin rings($duration, $delay) {
    opacity: 0;
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    position: absolute;
    // top: -8px;
    // left: -8px;
    right: 0;
    bottom: 0;
    content: '';
    height: 100%;
    width: 100%;
    border: 5px solid #c41f1f33;
    border-radius: 100%;
    
    z-index: -1;
}

.ripple-counter {
    position: relative;
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    // height: 40px;
    width: 40px;
    border-radius: 100%;
    background: #FFFFFF;
    box-shadow: 0 0 20px 0 rgba(0,0,0,0.25);
    z-index: 1;
    cursor: pointer;
    span {
        position: relative;
        font-size: 15px;
        font-weight: 600;
        // top: 5px;
        // left: -5px;
    }
    

    &::after {
        @include rings(3s, 0s);
    }
    
    // &::before {
    //     @include rings(2s, 0.5s);
    // }
}

@keyframes ripple {
  from {
    opacity: 1;
    transform: scale3d(0.75,0.75,1);
  }
  
  to {
    opacity: 0;
    transform: scale3d(1.5,1.5,1);
  }
}
</style>