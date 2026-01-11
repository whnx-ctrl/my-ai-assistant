// ==================== 配置区域 ====================
// 重要：将 YOUR_SERVER_IP 替换为你的服务器公网IP，端口为8000
const API_BASE_URL = 'http://175.178.109.106:8000';
// =================================================

// 获取DOM元素
const questionInput = document.getElementById('questionInput');
const askButton = document.getElementById('askButton');
const displayQuestion = document.getElementById('displayQuestion');
const displayAnswer = document.getElementById('displayAnswer');
const loadingIndicator = document.getElementById('loadingIndicator');
const statusIndicator = document.getElementById('statusIndicator');
const apiResult = document.getElementById('apiResult');

// 1. 页面加载时检查服务器状态
window.addEventListener('load', function() {
    checkServerStatus();
});

// 2. 检查服务器连接状态
async function checkServerStatus() {
    statusIndicator.innerHTML = '<i class="fas fa-circle-notch fa-spin"></i> 检测中...';
    
    try {
        const response = await fetch(`${API_BASE_URL}/`, { timeout: 5000 });
        if (response.ok) {
            const data = await response.json();
            statusIndicator.innerHTML = `<i class="fas fa-check-circle" style="color:#28a745"></i> 在线 (${data.status})`;
            statusIndicator.style.color = '#28a745';
        } else {
            throw new Error(`HTTP ${response.status}`);
        }
    } catch (error) {
        console.error('状态检查失败:', error);
        statusIndicator.innerHTML = `<i class="fas fa-exclamation-triangle" style="color:#dc3545"></i> 连接异常`;
        statusIndicator.style.color = '#dc3545';
    }
}

// 3. 核心功能：向AI提问
async function askQuestion() {
    const question = questionInput.value.trim();
    
    if (!question) {
        alert('请输入您的问题');
        questionInput.focus();
        return;
    }
    
    // 更新UI状态
    askButton.disabled = true;
    askButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> 思考中...';
    displayQuestion.textContent = question;
    displayAnswer.innerHTML = '...';
    loadingIndicator.style.display = 'block';
    
    try {
        // 调用后端API
        const startTime = Date.now();
        const response = await fetch(`${API_BASE_URL}/chat?q=${encodeURIComponent(question)}`);
        const endTime = Date.now();
        const responseTime = endTime - startTime;
        
        if (!response.ok) {
            throw new Error(`请求失败 (HTTP ${response.status})`);
        }
        
        const data = await response.json();
        
        // 显示结果
        displayAnswer.innerHTML = data.answer.replace(/\n/g, '<br>');
        
        // 在控制台输出详细信息（用于调试）
        console.log(`提问: "${question}" | 响应时间: ${responseTime}ms`);
        console.log('完整响应:', data);
        
    } catch (error) {
        console.error('API调用错误:', error);
        displayAnswer.innerHTML = `<span style="color:#dc3545">请求失败: ${error.message}</span><br>
                                  <small>请检查：1. 后端服务是否运行？ 2. 防火墙设置？</small>`;
    } finally {
        // 恢复UI状态
        askButton.disabled = false;
        askButton.innerHTML = '<i class="fas fa-paper-plane"></i> 发送提问';
        loadingIndicator.style.display = 'none';
        questionInput.focus();
    }
}

// 4. API端点测试功能
window.testEndpoint = async function(endpoint) {
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`);
        const data = await response.json();
        
        // 美化JSON显示
        apiResult.textContent = JSON.stringify(data, null, 2);
        apiResult.style.borderLeft = '4px solid #28a745';
    } catch (error) {
        apiResult.textContent = `错误: ${error.message}\n\n请确保：\n1. 后端服务正在运行 (${API_BASE_URL})\n2. 端口8000已开放`;
        apiResult.style.borderLeft = '4px solid #dc3545';
    }
};

// 5. 绑定事件
askButton.addEventListener('click', askQuestion);

questionInput.addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        askQuestion();
    }
});

// 6. 示例问题快捷输入（可选功能）
function insertExample(exampleText) {
    questionInput.value = exampleText;
    questionInput.focus();
}

// 在控制台输出初始化信息
console.log(`前端已加载，API基础地址: ${API_BASE_URL}`);
console.log('提示：可以在控制台调用 insertExample("你的问题") 来快速测试');
