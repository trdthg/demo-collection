#[macro_use]
extern crate clap;

use chrono::Utc;
use clap::App;

use rsbook::*;

fn main() {
    let args = std::env::args();
    println!("{:?}", args);
    let mut project_name;
    let mut base_dir;
    let start_time = Utc::now().timestamp_millis() as f64;
    let yaml = load_yaml!("cli.yml");
    let matches = App::from_yaml(yaml).get_matches();
    if let Some(new_matches) = matches.subcommand_matches("new") {
        // 得到文件base路径
        project_name = new_matches.value_of("PROJECT_NAME").unwrap();
        base_dir = new_matches.value_of("base_dir").unwrap_or(".");
        // 创建基本文件结构
        println!("creating new project {} in {} ... ", project_name, base_dir);
        let project_name = &format!("{}/{}",  base_dir, project_name);
        booknew(project_name);
    }

    if let Some(build_matches) = matches.subcommand_matches("build") {
        // 得到文件base路径
        project_name = build_matches.value_of("PROJECT_NAME").unwrap();
        base_dir = build_matches.value_of("base_dir").unwrap_or(".");
        // 创建基本文件结构
        println!("creating new project {} in {} ... ", project_name, base_dir);
        let project_name = &format!("{}/{}",  base_dir, project_name);
        bookbuild(project_name);
    }

    if let Some(_) = matches.subcommand_matches("clean") {
        let project_name = "tmp";
        println!("building project {} ... ", project_name);
        bookclean(project_name);
    }
    let end_time = Utc::now().timestamp_millis() as f64;
    println!("{}", "BUILD SUCCESS");
    println!("Total time: {} s", (end_time - start_time) / 1000.00);
    println!("Finished at: {}", Utc::now().to_string())
}
