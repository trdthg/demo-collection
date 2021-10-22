use std::fs;
use std::fs::File;
use std::io::prelude::*;
use std::io;
use std::path::Path;
use std::time::{ Duration, SystemTime};

pub fn create_dirs(dir: &str) {
    if !Path::new(dir).exists() {
        match fs::create_dir_all(dir) {
            Err(why) => panic!("create {}: {}", dir, why.to_string()),
            Ok(_) => println!("create {}", dir),
        };
    }
}

pub fn create_file(path: &str) {
    let path = Path::new(&path);
    match File::create(path) {
        Err(why) => panic!("create {}: {}", path.display(), why.to_string()),
        Ok(file) => file,
    };
    // match file_index_md.write_all(content.as_bytes()) {
    //     Err(why) => panic!("write {}: {}", fpath.display(), why.to_string()),
    //     Ok(_) => println!("write {}", path.display()),
    // };
}

pub fn write_file(path: &str, content: &str) {
    let mut f = File::create(path).unwrap();
    f.write_all(content.as_bytes()).unwrap();
}

pub fn get_changetime(path_str: &str) -> u64 {
    let file = File::open(path_str).unwrap();
    let metadata = file.metadata().unwrap();
    let mtime = metadata.modified().unwrap();
    let secs = match mtime.duration_since(SystemTime::UNIX_EPOCH) {
        Ok(duration) => duration.as_secs(),
        Err(_) => 0,
    };
    secs
}

pub fn get_file_info(path: &str) -> io::Result<FileInfo> {
    let path = Path::new(path);
    // let file_name: Option<String> = path.file_name().map(|file_name| file_name.to_string_lossy().to_string());
    // if let Some(file_name) = path.file_name() {
        //     let file_name = file_name.to_string_lossy().to_string();
        // }
        // let file_name = path.file_name()?.to_string_lossy().to_string();
    let file_name: String;
    match path.file_name().ok_or(io::Error::from(io::ErrorKind::NotFound)) {
        Ok(name) => file_name = name.to_string_lossy().to_string(),
        Err(e) => return Err(e), 
    }
    let mut file = File::open(path)?;
    let mut content = String::new();
    file.read_to_string(&mut content)?;
    let metadata = file.metadata()?;
    let mtime = metadata.modified()?;
    let modify_secs: u64 = match mtime.duration_since(SystemTime::UNIX_EPOCH) {
        Ok(n) => n.as_secs(),
        Err(_) => 0,
    };

    Ok(FileInfo {
        file_name,
        content,
        modify_secs,
    })

}

pub struct FileInfo {
    pub file_name: String,
    pub content: String,
    pub modify_secs: u64,
}

#[cfg(test)]
pub mod test {

    #[test]
    fn demo() {}
}
