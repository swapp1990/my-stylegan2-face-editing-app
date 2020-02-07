<template>
    <div class="btnContainer">
        <button class="ti-btn" ref="tiBtn" v-on:click="animateRipple">
            <slot></slot>
            <span
                class="ripple"
                v-bind:ref="'ripple-' + i"
                v-for="(val, i) in ripples"
                v-if="val !== null"
                v-bind:style="{'top': val.y + 'px', 'left': val.x + 'px'}"
                v-on:animationend="rippleEnd(i)">
            </span>
        </button>
    </div>
</template>

<script>
    export default {
        name: "ripple-btn",
        props: ['text'],
        data: function() {
            return {
                ripples: []
            }
        },
        methods: {
            animateRipple: function(e) {
                let el  = this.$refs.tiBtn;
                let pos = el.getBoundingClientRect();
                
                this.ripples.push({
                    x: e.clientX - pos.left,
                    y: e.clientY - pos.top
                });

                this.$emit('click', e);
            },
            rippleEnd: function(i) {
                this.ripples.splice(i, 1);
            }
		},
    }
</script>

<style scoped lang="scss">
$black: #000;
$white: #fff;
$shocking-pink: #ff1ead;

.btnContainer {
    font-family: Inconsolata, monospace;
	font-size: 24px;
    // background-color: $black;
}

.ti-btn {
    width: 40px;
	height: 40px;
    background-color: #eee;
	color: $white;
	font: inherit;
	border: 0;
    border-radius: 1.125em;
    box-shadow:
    -0.2em -0.125em 0.125em rgba(0, 0, 0, 0.25), 
    0 0 0 0.04em rgba(0, 0, 0, 0.3), 
    0.02em 0.02em 0.02em rgba(0, 0, 0, 0.4) inset, 
    -0.05em -0.05em 0.02em rgba(255, 255, 255, 0.8) inset;
	// padding: 20px 30px;
	overflow: hidden;
    outline: none;
	display: inline-block;
	position: relative;
}

.ripple {
	background-color: $shocking-pink;
	width: 1rem;
	height: 1rem;
	position: absolute;
	border-radius: 50%;
	transform: translateX(-100%) translateY(-100%);
	mix-blend-mode: screen;
	animation: rippleAnim 1000ms ease-out forwards;
}

@keyframes rippleAnim {
    0%   { transform: translate(-100%, -100%); }
    80%  { transform: translate(-100%, -100%) scale(50); }
    100% { transform: translate(-100%, -100%) scale(50); opacity: 0; }
}
</style>