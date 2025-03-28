// script.js
/*
  JS核心方法库：
  1. DOM操作: getElementById, querySelector
  2. 事件系统: addEventListener
  3. 样式控制: style.property, classList
  4. 数据操作: JSON.parse/stringify
  5. 异步操作: fetch, async/await
  6. 数组方法: map, filter, reduce
  7. 函数式编程: 箭头函数, 闭包
*/

// 元素获取
const colorBtn = document.getElementById('colorBtn');
const mainCard = document.getElementById('mainCard');

// 颜色状态
let isBlueTheme = true;

// 事件监听
colorBtn.addEventListener('click', () => {
  // 类名切换
  mainCard.classList.toggle('active');
  
  // 样式直接修改
  mainCard.style.backgroundColor = isBlueTheme ? '#f1c40f' : '#3498db';
  
  // 条件逻辑
  if(isBlueTheme) {
    colorBtn.textContent = '恢复蓝色主题';
  } else {
    colorBtn.textContent = '切换黄色主题';  
  }
  
  isBlueTheme = !isBlueTheme;
});

// 定时器示例
setTimeout(() => {
  mainCard.style.transform = 'scale(1.05)';
}, 1000);