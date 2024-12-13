<script>
	import Vattenfall from '$lib/vattenfall.png';
	import '../app.css';
</script>

<div class="fixed flex h-full min-h-screen w-full flex-col overflow-hidden">
	<header class="bg-primary flex h-16 w-full items-center justify-between px-4 shadow-md sm:px-8">
		<div class="flex items-center justify-between gap-4 sm:gap-10">
			<img src={Vattenfall} class="h-12 w-auto rounded-full bg-white p-1" alt="Vattenfall" />
			<h1 class="font-mono text-xl text-white sm:text-2xl md:text-3xl">Tax Code Predictor</h1>
		</div>
		<div>
			<img
				loading="lazy"
				class="h-8 w-auto"
				src="https://www.capgemini.com/wp-content/themes/capgemini2020/assets/images/logo-white.svg"
				alt="Capgemini"
				data-blue-logo-src="https://www.capgemini.com/wp-content/themes/capgemini2020/assets/images/logo.svg"
				data-white-logo-src="https://www.capgemini.com/wp-content/themes/capgemini2020/assets/images/logo-white.svg"
			/>
		</div>
	</header>
	<main class="flex-grow overflow-auto bg-gray-100 p-4 sm:p-6">
		<slot></slot>
	</main>
</div>
