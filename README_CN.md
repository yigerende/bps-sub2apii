> **bps-sub2api 独立部署版**：基于 [ranxi2001/sub2api](https://github.com/ranxi2001/sub2api)，应用、PostgreSQL、Redis、网络和持久化存储使用独立名称，默认宿主机端口 `8082`。部署及升级请先看 [BPS 部署说明](docs/BPS_DEPLOY.md)。本仓库地址为 [yigerende/bps-sub2apii](https://github.com/yigerende/bps-sub2apii)，镜像为 `ghcr.io/yigerende/bps-sub2api:latest`。下文保留上游功能介绍及贡献者信息。

# bps-sub2api 中文说明

中文已作为本仓库的默认文档，请阅读 [README.md](README.md)。

[部署方式](README.md#部署方式) · [使用文档](https://tosky.io/docs/) · [版本下载](https://github.com/ranxi2001/sub2api/releases)

## OpenAI 图片输出格式

OAuth / Setup Token 的 GPT Image 1.5、2、2.5、2.6 图片请求以映射后模型调用 Codex 原生端点；2.6 之前的模型保留端点 404/405 时回退 Responses，2.6 不回退。`output_format` / `output_compression` 透传不保证上游按指定格式输出：请求 JPEG/SVG 仍可能返回 4xx 或 HTTP 200、`output_format: "png"` 及 PNG 内容，包括已报告的 `gpt-image-2.5-flare` JPEG 请求。保存或交付前，应核对返回字段（含图片项字段）和真实图片格式，以实际格式设置扩展名和 MIME。成功响应保留状态、内容及 usage；格式不符仍可能计费，自动重试可能重复生成并计费。
