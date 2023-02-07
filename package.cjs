/* eslint-env node */
const fs = require('fs');
const path = require('path');
const { version } = require('./package.json');

const sourcePath = (...paths) => (
    path.join(__dirname, ...paths)
);

const TARGET_NAME = `志愿服务信息管理系统v${version}`;
const TARGET_DIR = sourcePath('releases', TARGET_NAME);

const targetPath = (...paths) => (
    path.join(TARGET_DIR, ...paths)
);

function copyDirSync(src, dest) {
    fs.cpSync(src, dest, {
        recursive: true,
    });
}

// reset output directory
if (fs.existsSync(TARGET_DIR)) {
    fs.rmdirSync(TARGET_DIR);
}
fs.mkdirSync(TARGET_DIR);
fs.mkdirSync(targetPath('data'));
fs.mkdirSync(targetPath('output'));
fs.mkdirSync(targetPath('backup'));

// copy backend files
copyDirSync(
    sourcePath('backend'),
    targetPath('backend'),
);

// copy frontend files
copyDirSync(
    sourcePath('dist'),
    targetPath('frontend'),
);

// copy template files
copyDirSync(
    sourcePath('template'),
    targetPath('template'),
);

// copy other files
fs.copyFileSync(
    sourcePath('LICENSE'),
    targetPath('LICENSE'),
);
fs.copyFileSync(
    sourcePath('scripts/launch.bat'),
    targetPath('启动（Windows）.bat'),
);
fs.copyFileSync(
    sourcePath('scripts/launch.bash'),
    targetPath('启动（MacOS/Linux）.bash'),
);
fs.copyFileSync(
    sourcePath('scripts/install-deps.bat'),
    targetPath('安装依赖（Windows）.bat'),
);
fs.copyFileSync(
    sourcePath('scripts/install-deps.bash'),
    targetPath('安装依赖（MacOS/Linux）.bash'),
);
fs.copyFileSync(
    sourcePath('docs/documentation.pdf'),
    targetPath('使用手册.pdf'),
);
