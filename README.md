# CyberGIS Compute Hello World Example
Example project on how to modify your code to run on CyberGIS Compute.

## Specify How You'd Like to Run Your Project
Include a `manifest.json` file under your project's root path. It defines how your projects would run on `HPC`. 

In the file, you should include some basic information like:
- `name: string`: name of the project
- `description: string`: a brief description
- `container: string`: the container environment to run your code on
  - available containers: `python`
  - for custom container environment, contact xxx@illinois.edu
- `supported_hpc?: Array<string>`: supported computing resources, see [doc](https://github.com/cybergis/cybergis-compute-core#supported-hpc--computing-resources). Default `['keeling_community']`
- `default_hpc?: string`: default computing resources. Default to first defined in `supported_hpc`

**Then**, you should define the execution steps for your project:
1. `pre_processing_stage?: string`: an *optional* bash command that runs when the project begins. Single threaded, non-MPI.
2. `execution_stage: string`: the **required** bash command that runs in multi-threaded MPI and executes the project.
   - if you'd like to run sbatch command, use `execution_stage_in_raw_sbatch: Array<string>`
3. `post_processing_stage?: string`: an *optional* bash command that runs after execution finishes. Single threaded, non-MPI.

**After that**, define how you'd like your users to interact with your project by passing in **parameters**. Define your parameters in `param_rules?: {[keys: string]: any}` like:
```javascript
{
    // ...
     "param_rules": {
         // define a string input
        "input_a": {
            "type": "integer",
            "require": true,
            "max": 100,
            "min": 0,
            "default_value": 50,
            "step": 10
        },
        // define a select options input
        "input_b": {
            "type": "string_option",
            "options": ["foo", "bar"],
            "default_value": "foo"
        }
    }
}
```

**Finally**, define the `HPC` resources you'd like to use. Supported types are:
```javascript
{
    // ...
    "slurm_input_rules": {
        "num_of_node": integerRule,     // number of nodes, ie. SBATCH nodes
        "num_of_task": integerRule,     // number of tasks, ie. SBATCH ntasks
        "time": integerRule,            // runtime limit, ie. SBATCH time
        "cpu_per_task": integerRule,    // number of CPU per task, ie. SBATCH cpus-per-task
        "memory_per_cpu": integerRule,  // amount of memory per CPU, ie. SBATCH mem-per-cpu
        "memory_per_gpu": integerRule,  // amount of memory per GPU, ie. SBATCH mem-per-gpu
        "memory": integerRule,          // total memory allocated, ie. SBATCH mem
        "gpus": integerRule,            // total GPU allocated, ie. SBATCH gpus
        "gpus_per_node": integerRule,   // number of GPU per node, ie. SBATCH gpus-per-node
        "gpus_per_socket": integerRule, // number of GPU per socket, ie. SBATCH gpus-per-socket
        "gpus_per_task": integerRule,   // number of GPU per task, ie. SBATCH gpus-per-task
        "partition": stringOptionRule   // partition name on HPC, ie. SBATCH partition
    }
}
```

`integerRule` type configs are defined as such:
```javascript
{
    "slurm_input_rules": {
        // regular integer values
        "num_of_task": {
            "max": 6,
            "min": 1,
            "default_value": 4,
            "step": 1
        },
        // united specific configs like
        // 'GB' | 'MB' | 'Minutes' | 'Hours' | 'Days'
        "time": {
            "max": 50,
            "min": 10,
            "default_value": 20,
            "step": 1,
            "unit": "Minutes"
        }
    }
}
```

`stringOptionRule` can be defined as such:
```javascript
{
    "slurm_input_rules": {
        // ...
        "partition": {
            "type": "string_option",
            "options": ["option_a", "option_b", "option_c"],
            "default_value": "option_a"
        }
    }
}
```

## How to Read Input Parameters and Other Job information?
CyberGIS Compute creates a `job.json` file that includes:
```javascript
{
   "job_id": string,
   "user_id": string,
   "hpc": string,
   // user parameters input
   "param": {
       "param_a": 1,
       "param_b": "value"
   },
   "executable_folder": string, // path to the executable code
   "data_folder": string, // path to the uploaded data
   "result_folder": string // path to the download data folder
}
```

If your application does not support reading JSON file, you can access it through system environment variables
```python
import os
os.environ['job_id']
os.environ['param_param_a'] # access param['param_a']
```

## Some Tips
1. Because CyberGIS Compute downloads the `result_folder` using globus, we recommend putting downloadable data into the `result_folder`. You can get the full path in `job.json`.
2. If you want to execute multiple command (ex. setup something), you can create a bash script and just run `bash some_script.sh` in your `execution_stage`.