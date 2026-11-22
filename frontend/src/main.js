
import { mount } from 'svelte'
import App from './App.svelte'
import './app.css'
import './styles/global.css'

const target = document.getElementById('app')

if (!target) {
    throw new Error('Elemento #app não encontrado no HTML')
}

const app = mount(App, {
    target
})

export default app

