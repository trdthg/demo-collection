use std::path::Path;

use crate::util::file::*;
use crate::util::parse::*;
use crate::Config;

use std::fs;

use comrak::{markdown_to_html, ComrakOptions};
use regex::Regex;

pub fn create_default_index(docs: &str, dist: &str, config: &Config) {
    let content = fs::read_to_string("assets/index.html").unwrap();

    // title
    let re_module = Regex::new(r"\{\{\s*title\s*\}\}").unwrap();
    let content = &String::from(re_module.replace_all(&content, &config.title));

    // index
    let re_module = Regex::new(r"\{\{\s*index\s*\}\}").unwrap();
    let content = &String::from(re_module.replace_all(&content, "index.html"));

    // nav_links
    let re_module = Regex::new(r"\{\{\s*links\s*\}\}").unwrap();
    let links = get_links_index(&config.nav_map);
    let content = &String::from(re_module.replace_all(content, links));

    // sidebar_content
    let re_module = Regex::new(r"\{\{\s*sidebar_content\s*\}\}").unwrap();
    let sidebar_content = get_titles("assets/README.md");
    let content = &String::from(re_module.replace_all(content, sidebar_content));

    // page_content
    let re_module = Regex::new(r"\{\{\s*page_content\s*\}\}").unwrap();
    let md_content = fs::read_to_string(format!("{}/README.md", docs)).unwrap();
    let md_html = markdown_to_html(&md_content, &ComrakOptions::default());
    let content = &String::from(re_module.replace_all(content, md_html));

    // create new index file
    let default_config_file = &format!("{}/{}", dist, "index.html");
    let config_file = Path::new(default_config_file);
    write_file(config_file.to_str().unwrap(), content);
}

pub fn create_all(docs: &str, dist: &str, config: &Config) {

    let map = &config.sidebar_map;
    for (k, v) in map {
        let folder_name = k;
        create_dirs(&format!("{}/{}",dist, folder_name));
        let mut sidebars = String::new();
        let mut contents: Vec<String> = Vec::new();
        for file_name in v {
            let content = fs::read_to_string("assets/other.html").unwrap();
            let md = &format!("{}/{}/{}.md", docs, folder_name, file_name);
            // title
            let re_module = Regex::new(r"\{\{\s*title\s*\}\}").unwrap();
            let content = &String::from(re_module.replace_all(&content, &config.title));

            // index
            let re_module = Regex::new(r"\{\{\s*index\s*\}\}").unwrap();
            let content = &String::from(re_module.replace_all(&content, "../index.html"));

            // nav_links
            let re_module = Regex::new(r"\{\{\s*links\s*\}\}").unwrap();
            let links = get_links(&config.nav_map);
            let content = &String::from(re_module.replace_all(content, links));


            // page_content && sidebar_content
            let md_content = fs::read_to_string(md).unwrap();
            let md_html = markdown_to_html(&md_content, &ComrakOptions::default());
            let (md_html, sidebar_content) = get_titles_from_html(&md_html, &file_name);

            let re_module = Regex::new(r"\{\{\s*page_content\s*\}\}").unwrap();
            let content = String::from(re_module.replace_all(content, md_html));
            
            sidebars.push_str(&sidebar_content);
            contents.push(content);
        }
        for i in 0..v.len() {
            let file_name = &v[i];
            let content = &contents[i];
            let re_module = Regex::new(r"\{\{\s*sidebar_content\s*\}\}").unwrap();
            let content = &String::from(re_module.replace_all(content, &sidebars));
            // create new index file
            let default_config_file = &format!("{}/{}/{}.html", dist, folder_name, file_name);
            let config_file = Path::new(default_config_file);
            println!("{}", config_file.display());
            write_file(config_file.to_str().unwrap(), content);
        }
    }

}

pub fn create_github_min_css(dist: &str) {
    let content = &fs::read_to_string("assets/css/prism.css").unwrap();
    let default_config_file = &format!("{}/{}", dist, "assets/css/prism.css");
    let config_file = Path::new(default_config_file);
    write_file(config_file.to_str().unwrap(), content);
}

pub fn create_index_css(dist: &str) {
    let content = &fs::read_to_string("assets/css/index.css").unwrap();
    let default_config_file = &format!("{}/{}", dist, "assets/css/index.css");
    let config_file = Path::new(default_config_file);
    write_file(config_file.to_str().unwrap(), content);
}

pub fn creage_highlight_min_js(dist: &str) {
    let content = &fs::read_to_string("assets/js/prism.js").unwrap_or("sss".to_string());
    let default_config_file = &format!("{}/{}", dist, "assets/js/prism.js");
    let config_file = Path::new(default_config_file);
    write_file(config_file.to_str().unwrap(), content);
}

pub fn create_default_config(project_name: &str) {
    // create default config file
    let content = &fs::read_to_string("assets/config.json").unwrap();
    let default_config_file = &format!("{}/{}", project_name, "docs/.rsbook/config.json");
    let config_file = Path::new(default_config_file);
    write_file(config_file.to_str().unwrap(), content);
}

pub fn create_hello_vue(project_name: &str) {
    let content = r#"
    <template>
    <div>
        <h1 class="h1">Hello World</h1>
    </div>
    </template>

    <style scoped>
    h1 {
        color: rgb(209, 88, 88);
    }
    </style>

    <script>
    export default {
        
    }
    </script>
    "#;
    let default_config_file = &format!("{}/{}", project_name, "docs/.rsbook/components/hello.vue");
    let config_file = Path::new(default_config_file);
    write_file(config_file.to_str().unwrap(), content);
}

pub fn create_readme(project_name: &str) {
    let content = &fs::read_to_string("assets/README.md").unwrap();
    // let md_html = markdown_to_html(&md_content, &ComrakOptions::default());
    let default_config_file = &format!("{}/{}", project_name, "docs/README.md");
    let config_file = Path::new(default_config_file);
    write_file(config_file.to_str().unwrap(), content);
}
