<template>
<div class="frame">
	<div class="range">
		<div class="p-1">
			<button type="button" class="transBtn" @click="decCoeff()"><i class='fas fa-minus'></i></button>
		</div>
		<input type="range" :min="min" :max="max" step="0.25" v-model="currAttrVal_l" @change="attrChanged">
		<div class="p-1">
			<button type="button" class="transBtn" @click="incCoeff()"><i class='fas fa-plus'></i></button>
		</div>
	</div>
</div>
</template>

<script>
    export default {
        name: 'rangeslider',
        props: {
            min: {
                type: Number,
                default: 0
            },
            max: {
                type: Number,
                default: 10
            },
            initVal: {
                type: Number,
                default: 0
            }
        },
        watch: {
            initVal: {
                immediate: true,
                deep: true,
                handler(val, oldVal) {
                    this.currAttrVal_l = val;
                },
            },
        },
        data() {
            return {
                currAttrVal_l: 0
            }
        },
        mounted() {
            this.currAttrVal_l = this.initVal;
        },
        methods: {
            attrChanged() {
                this.$emit("changedAttr", this.currAttrVal_l);
			},
			incCoeff() {
				this.currAttrVal_l += 0.25;
				this.$emit("changedAttr", this.currAttrVal_l);
			},
			decCoeff() {
				this.currAttrVal_l -= 0.25;
				this.$emit("changedAttr", this.currAttrVal_l);
			}
        }
    }
</script>

<style lang="scss" scoped>
$color-bg: #f5f6f7;
.frame {
	display: flex;
	align-items: center;
	justify-content: center;
    opacity: 1;
    transition: opacity .5s ease-in-out;
}

.range {
	background: rgba(#f5f6f7, 0.3);
	height: 2rem;
	width: 80%;
	border-radius: 5rem;
	box-shadow: 1px 5px 5px rgba(black, 0.3);

	display: flex;
	align-items: center;
	justify-content: space-between;
}

$color-red: #d30320;
.transBtn {
	border: none;
	background: none;
	outline: none;
	&:hover {
		outline: none;
		// background: darken(rgba($color-red, .95), 8%);
	}
}

input[type="range"] {
	-webkit-appearance: none;
	width: 80%;
	height: 100%;
	background: transparent;
	&:focus {
		outline: none;
	}

	//WEBKIT
	&::-webkit-slider-thumb {
		-webkit-appearance: none;
		height: 16px;
		width: 16px;
		border-radius: 50%;
		background: rgba($color-bg, 0.9);
		margin-top: -5px;
		box-shadow: 1px 1px 2px rgba(#000, 0.9);
		cursor: pointer;
	}

	&::-webkit-slider-runnable-track {
		width: 60%;
		height: 9px;
		background: rgba(#000, 0.5);
		border-radius: 3rem;

		transition: all 0.5s;
		cursor: pointer;
	}

	&:hover::-webkit-slider-runnable-track {
		background: darken(rgba($color-red, .95), 8%);
	}
    &:focus::-webkit-slider-runnable-track {
		background: darken(rgba($color-red, .95), 8%);
	}

	// IE

	&::-ms-track {
		width: 60%;
		cursor: pointer;
		height: 9px;

		transition: all 0.5s;
		/* Hides the slider so custom styles can be added */
		background: transparent;
		border-color: transparent;
		color: transparent;
	}

	&::-ms-thumb {
		height: 16px;
		width: 16px;
		border-radius: 50%;
		background: #ffffff;
		margin-top: -5px;
		box-shadow: 1px 1px 2px rgba(#000, 0.5);

		cursor: pointer;
	}

	&::-ms-fill-lower {
		background: #bdbdbd;
		border-radius: 3rem;
	}
	&:focus::-ms-fill-lower {
		background: #ff6e40;
	}
	&::-ms-fill-upper {
		background: #bdbdbd;
		border-radius: 3rem;
	}
	&:focus::-ms-fill-upper {
		background: #ff6e40;
	}

	//FIREFOX
	&::-moz-range-thumb {
		height: 16px;
		width: 16px;
		border-radius: 50%;
		background: #ffffff;
		margin-top: -5px;
		box-shadow: 1px 1px 2px rgba(#000, 0.5);

		cursor: pointer;
	}

	&::-moz-range-track {
		width: 60%;
		height: 9px;
		background: #bdbdbd;
		border-radius: 3rem;

		transition: all 0.5s;
		cursor: pointer;
	}
	&:hover::-moz-range-track {
		background: $color-red;
	}
}

</style>