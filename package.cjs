/* eslint-env node */
const fs = require('fs');
const path = require('path');
const { version } = require('./package.json');

const BASE_PATH = path.join(__dirname, 'releases');
const TARGET_NAME = `志愿服务信息管理系统v${version}`;
const TARGET_PATH = path.join(BASE_PATH, TARGET_NAME);

// reset output directory
if (fs.existsSync(TARGET_PATH)) {
    fs.rmdirSync(TARGET_PATH);
}
fs.mkdirSync(TARGET_PATH);
fs.mkdirSync(path.join(TARGET_PATH, 'backup'));
fs.mkdirSync(path.join(TARGET_PATH, 'output'));

// copy backend files
fs.cpSync(
    path.join(BASE_PATH, 'backend'),
    path.join(TARGET_PATH, 'backend'),
);

// copy frontend files
fs.cpSync(
    path.join(BASE_PATH, 'dist'),
    path.join(TARGET_PATH, 'dist'),
);

// copy template files
fs.cpSync(
    path.join(BASE_PATH, 'template'),
    path.join(TARGET_PATH, 'template'),
);

// copy other files
fs.copyFileSync(
    path.join(BASE_PATH, 'launch.bat'),
    path.join(TARGET_PATH, '启动.bat'),
);
fs.copyFileSync(
    path.join(BASE_PATH, 'launch.bash'),
    path.join(TARGET_PATH, '启动.bash'),
);
fs.copyFileSync(
    path.join(BASE_PATH, 'docs/documentation.pdf'),
    path.join(TARGET_PATH, '说明书.pdf'),
);
