pub mod template;
pub mod util;

use std::collections::HashMap;
use std::fs::File;
use std::path::Path;

use util::file::*;

#[derive(Debug)]
pub struct Config {
    pub title: String,
    pub icon: String,
    pub nav_map: HashMap<String, String>,
    pub sidebar_map: HashMap<String, Vec<String>>,
}

pub fn bookbuild(project_name: &str) {
    println!("+-- reading conf...");
    let config: Config = bookbuild_read_config(project_name);
    println!("+-- building dirs...");
    bookbuild_newdir(".", project_name);

    println!("+-- creating templates...");
    // 创建模板文件
    let dist = &format!("{}/docs/.rsbook/dist", project_name);
    let docs = &format!("{}/docs", project_name);
    // template::create_README(dist);
    template::create_default_index(docs, dist, &config);
    template::create_all(docs, dist, &config);
    template::create_index_css(dist);
    template::create_github_min_css(dist);
    template::creage_highlight_min_js(dist);
}

pub fn bookbuild_read_config(project_name: &str) -> Config {
    let config_file = File::open(format!(
        "{}/{}/{}/{}",
        project_name, "docs", ".rsbook", "config.json"
    ))
    .unwrap();
    // let mut content = String::new();
    // config_file.read_to_string(&mut content).unwrap();
    // let mut config = json::parse(&content).unwrap();

    let config: serde_json::Value = serde_json::from_reader(config_file).unwrap();

    let title: String = config["head"]["title"].as_str().unwrap_or("").to_string();
    let icon: String = config["head"]["icon"].as_str().unwrap_or("").to_string();
    // let sidebar = config["themeConfig"]["sidebar"];

    let mut nav_map: HashMap<String, String> = HashMap::new();
    let mut sidebar_map: HashMap<String, Vec<String>> = HashMap::new();
    // pub fn as_array(&self) -> Option<&Vec<Value>> {
    if let Some(vec) = config["nav"].as_array() {
        for elem in vec {
            nav_map.insert(
                elem["text"].as_str().unwrap().to_string(),
                elem["link"].as_str().unwrap().to_string(),
            );
        }
    }
    if let Some(vec) = config["themeConfig"]["sidebar"].as_array() {
        for elem in vec {
            if let Some(pages) = elem["pages"].as_array().take().map(|json| json) {
                let mut newpages: Vec<String> = Vec::new();
                for page in pages {
                    newpages.push(String::from(page.as_str().unwrap()));
                }
                sidebar_map.insert(elem["link"].as_str().unwrap().to_string(), newpages);
            }
        }
    }
    Config {
        title,
        icon,
        nav_map,
        sidebar_map,
    }
}

pub fn bookbuild_newdir(base_dir: &str, project_name: &str) {
    let dirs = vec!["assets/", "assets/js/", "assets/css", "assets/img"];
    let files = vec!["index.html"];
    for path in dirs {
        let temp: &str = &format!(
            "{}/{}/{}/{}",
            base_dir, project_name, "docs/.rsbook/dist", path
        );
        let temp = Path::new(temp);
        create_dirs(temp.to_str().unwrap());
    }
    for path in files {
        let temp: &str = &format!(
            "{}/{}/{}/{}",
            base_dir, project_name, "docs/.rsbook/dist", path
        );
        let temp = Path::new(temp);
        create_file(temp.to_str().unwrap());
    }
}

pub fn booknew(project_name: &str) {
    // 1. create dist menu
    let dirs = vec![
        "docs/.rsbook/",
        "docs/.rsbook/components/",
        "docs/.rsbook/public/",
        "docs/.rsbook/dist/",
        "docs/.rsbook/styles/",
    ];
    let files = vec![
        "docs/.rsbook/config.json",
        "docs/README.md",
        "deploy.sh",
        "deploy.cmd",
    ];
    for path in dirs {
        let temp: &str = &format!("{}/{}", project_name, path);
        let temp = Path::new(temp);
        create_dirs(temp.to_str().unwrap());
    }
    for path in files {
        let temp: &str = &format!("{}/{}", project_name, path);
        let temp = Path::new(temp);
        create_file(temp.to_str().unwrap());
    }

    template::create_default_config(project_name);
    template::create_hello_vue(project_name);
    template::create_readme(project_name);
}

pub fn bookclean(project_name: &str) {
    println!("{}", project_name);
}
