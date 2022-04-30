<template>
	<div>
		<div class="card">{{ name }} + {{ var1 }}</div>
	</div>
</template>

<script>
	module.exports = {
		data: function() {
			return {
				var1: "super"
			}
		},
		name: 'Card',
		props: [
			'name'
		]
}
</script>

<style>
.card {
	padding: 5px;
	border:  2px solid blue;
	border-radius: 4px;
	background-color: green;
	margin-bottom: 5px;
}
</style>