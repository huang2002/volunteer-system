/* eslint-env node */
const fs = require('fs');
const path = require('path');
const { name: appName, version: appVersion } = require('./package.json');

// Expected Release Structure:
// releases/<TARGET_NAME>v<VERSION>
//     +- output/
//     +- <PROJECT_NAME>.pyz
//     +- 初始化（Windows）.bat
//     +- 初始化（MacOS或Linux）.bash
//     +- 启动（Windows）.bat
//     +- 启动（MacOS或Linux）.bash
//     +- 使用手册.pdf
//     +- LICENSE.txt
//     `- requirements.txt

const ENCODING = 'utf8';

const sourcePath = (...paths) => (
    path.join(__dirname, ...paths)
);

const TARGET_NAME = `志愿服务信息管理系统v${appVersion}`;
const RELEASE_DIR = sourcePath('releases');
const TARGET_DIR = path.join(RELEASE_DIR, TARGET_NAME);
if (fs.existsSync(TARGET_DIR)) {
    throw new Error(
        `target directory already exists: ${TARGET_DIR}`
    );
}

const targetPath = (...paths) => (
    path.join(TARGET_DIR, ...paths)
);

const copyDirSync = (src, dest) => {
    fs.cpSync(src, dest, {
        recursive: true,
    });
};

const replacements = {
    __APP_NAME__: appName,
};
const copyFileWithPlaceholders = (src, dest) => {
    let content = fs.readFileSync(src, {
        encoding: ENCODING,
    });
    Object.entries(replacements)
        .forEach(([placeholder, replacement]) => {
            content = content.replace(placeholder, replacement);
        });
    fs.writeFileSync(dest, content);
};

// init directories
if (!fs.existsSync(RELEASE_DIR)) {
    fs.mkdirSync(RELEASE_DIR);
}
fs.mkdirSync(TARGET_DIR);
fs.mkdirSync(targetPath('data'));
fs.mkdirSync(targetPath('backup'));
fs.mkdirSync(targetPath('output'));

copyDirSync(
    sourcePath('backend'),
    targetPath('backend'),
);
copyDirSync(
    sourcePath('dist'),
    targetPath('frontend'),
);

fs.copyFileSync(
    sourcePath('requirements.txt'),
    targetPath('requirements.txt'),
);
fs.copyFileSync(
    sourcePath('LICENSE'),
    targetPath('LICENSE.txt'),
);

copyFileWithPlaceholders(
    sourcePath('scripts/launch.bat'),
    targetPath('启动（Windows）.bat'),
);
copyFileWithPlaceholders(
    sourcePath('scripts/launch.bash'),
    targetPath('启动（MacOS或Linux）.bash'),
);

fs.copyFileSync(
    sourcePath('scripts/init.bat'),
    targetPath('初始化（Windows）.bat'),
);
fs.copyFileSync(
    sourcePath('scripts/init.bash'),
    targetPath('初始化（MacOS或Linux）.bash'),
);

fs.copyFileSync(
    sourcePath('docs/documentation.pdf'),
    targetPath('使用手册.pdf'),
);

console.log(`Successfully packaged "${TARGET_NAME}"!`);
